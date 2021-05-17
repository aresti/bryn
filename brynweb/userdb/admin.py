from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html, mark_safe

from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin

from openstack.models import Region, Tenant
from .custom_filters import TeamLicenceFilter
from .models import (
    LicenceVersion,
    LicenceAcceptance,
    Team,
    Invitation,
    TeamMember,
    Profile,
)

from openstack.admin_scripts import setup_openstack_project, ExistingTenantError


def make_create_tenants_action(region):
    def create_tenants(modeladmin, request, queryset):
        n = 0
        for team in queryset:
            try:
                setup_openstack_project(team, region)
                n += 1
            except ExistingTenantError as e:
                modeladmin.message_user(request, str(e))
        modeladmin.message_user(request, f"Created {n} tenants at {region.name}")

    create_tenants.__name__ = f"create_{region.name}_tenants"
    create_tenants.short_description = f"Create {region.name} tenants"

    return create_tenants


class InvitationInline(InlineActionsMixin, admin.TabularInline):
    model = Invitation
    fields = ("email", "date", "made_by", "accepted")
    readonly_fields = ("email", "date", "made_by", "accepted")
    ordering = ["accepted", "-date"]

    def get_inline_actions(self, request, obj=None):
        actions = super().get_inline_actions(request, obj)
        if obj and not obj.accepted:
            actions.append("resend_invitation")
        return actions

    def has_add_permission(self, request, obj=None):
        return False

    def resend_invitation(self, request, obj, parent_obj):
        obj.send_invitation_email()
        messages.success(request, f"Resent invitation ({obj})")
        return None  # return to current changeform


class LicenceAcceptanceInline(admin.TabularInline):
    model = LicenceAcceptance
    readonly_fields = ["licence_version", "user", "accepted_at", "expiry"]
    ordering = ["-accepted_at"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TenantInline(admin.TabularInline):
    model = Tenant
    fields = [
        "tenant_link",
        "created_tenant_id",
        "created_tenant_name",
        "server_lease_links",
    ]
    readonly_fields = [
        "tenant_link",
        "created_tenant_id",
        "created_tenant_name",
        "server_lease_links",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def tenant_link(self, instance):
        url = reverse("admin:openstack_tenant_change", args=(instance.pk,))
        return format_html('<a href="{}">{}</a>', url, f"{instance.region.name} tenant")

    def server_lease_links(self, instance):
        links = []
        url_name = "admin:openstack_serverlease_change"
        for server_lease in instance.server_leases.filter(deleted=False):
            url = reverse(url_name, args=(server_lease.pk,))
            links.append(
                format_html('<a href="{}">{}</a>', url, f"{server_lease.server_name}")
            )
        return mark_safe("<br>".join(links))

    tenant_link.short_description = "Tenant"


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    fields = [
        "team_link",
        "user_link",
        "is_admin",
    ]
    readonly_fields = ["team_link", "user_link"]
    ordering = ["-is_admin"]

    def has_add_permission(self, request, obj=None):
        return False

    def team_link(self, instance):
        url = reverse("admin:userdb_team_change", args=(instance.team.id,))
        return format_html('<a href="{}">{}</a>', url, instance.team.name)

    team_link.short_description = "Team"

    def user_link(self, instance):
        url = reverse("admin:auth_user_change", args=(instance.user.id,))
        return format_html('<a href="{}">{}</a>', url, instance.user.username)

    user_link.short_description = "User"


class TeamAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "creator",
                    "institution",
                    "phone_number",
                    "default_region",
                    "verified",
                    "tenants_available",
                    "licence_expiry",
                    "licence_last_reminder_sent_at",
                ),
            },
        ),
        (
            "Registration info",
            {
                "classes": ("collapse",),
                "fields": (
                    "position",
                    "department",
                    "research_interests",
                    "intended_climb_use",
                    "held_mrc_grants",
                ),
            },
        ),
    )

    readonly_fields = ("id", "creator", "licence_last_reminder_sent_at")

    list_display = (
        "name",
        "id",
        "institution",
        "licence_expiry",
        "verified",
        "tenants_available",
    )
    list_filter = ("verified", "tenants_available", TeamLicenceFilter)

    search_fields = ("name", "institution")

    actions = [
        "verify_and_send_notification_email",
        "send_licence_renewal_reminder_emails",
    ]

    inlines = (
        TenantInline,
        TeamMemberInline,
        InvitationInline,
        LicenceAcceptanceInline,
    )

    def verify_and_send_notification_email(self, request, queryset):
        n = 0
        for t in queryset:
            t.verify_and_send_notification_email()
            n += 1
        self.message_user(request, "%s teams were sent notification email" % (n,))

    def send_licence_renewal_reminder_emails(self, request, queryset):
        for team in queryset:
            team.send_team_licence_reminder_emails()
            self.message_user(
                request,
                f"Licence renewal reminder emails sent for {queryset.count()} team(s)",
            )

    def get_actions(self, request):
        actions = super().get_actions(request)

        # Setup 'create tenant for region' actions
        active_regions = Region.objects.filter(disabled=False)
        for region in active_regions:
            action = make_create_tenants_action(region)
            actions[action.__name__] = (
                action,
                action.__name__,
                action.short_description,
            )

        return actions

    def save_model(self, request, obj, *args):
        # Set creator when manually creating a team
        if obj.creator is None:
            obj.creator = request.user
        super().save_model(request, obj, *args)


class TeamMemberAdmin(admin.ModelAdmin):
    autocomplete_fields = ("team", "user")


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = (
        "default_keypair",
        "default_team_membership",
        "new_email_pending_verification",
    )
    can_delete = False


class CustomUserAdmin(UserAdmin):
    list_filter = ("profile__email_validated",)
    actions = ("resend_email_activation_link",)
    inlines = (ProfileInline, TeamMemberInline)

    def resend_email_activation_link(self, request, queryset):
        for u in queryset:
            u.profile.send_validation_link()
        self.message_user(request, "Validation links resent.")


def model_str(obj):
    """Custom callable to enable use of model __str__ in list display"""
    return str(obj)


model_str.short_description = "Description"


class LicenceVersionAdmin(admin.ModelAdmin):
    list_display = (
        model_str,
        "effective_date",
        "validity_period_days",
    )


class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        model_str,
        "accepted",
        "date",
    )

    autocomplete_fields = ("to_team", "made_by")


admin.site.register(LicenceVersion, LicenceVersionAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
