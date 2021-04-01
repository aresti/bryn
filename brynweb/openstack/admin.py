from django.contrib import admin

from .models import (
    ActionLog,
    Tenant,
    Region,
    RegionSettings,
    ServerLease,
    ServerLeaseRequest,
)


def model_str(obj):
    """Custom callable to enable use of model __str__ in list display"""
    return str(obj)


model_str.short_description = "Description"


class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "created_tenant_name",
        "team",
    )

    search_fields = ("created_tenant_id", "created_tenant_name")


class ActionLogAdmin(admin.ModelAdmin):
    list_filter = ("error",)


class ServerLeaseAdmin(admin.ModelAdmin):
    list_display = (
        "server_name",
        "server_id",
        "team",
        "region",
        "last_renewed_at",
        "last_reminder_sent_at",
        "expiry",
        "renewal_count",
        "tenant",
        "user",
        "deleted",
        "shelved",
    )

    search_fields = ("server_id", "server_name")

    readonly_fields = (
        "server_id",
        "server_name",
        "last_renewed_at",
        "last_reminder_sent_at",
        "renewal_count",
        "tenant",
        "team",
        "region",
        "renewal_url",
        "deleted",
        "shelved",
    )

    actions = ("grant_indefinite_lease", "renew_lease", "send_renewal_reminder_email")

    def has_add_permission(self, request):
        return False

    def team(self, obj):
        return obj.tenant.team

    def user(self, obj):
        return obj.assigned_teammember.user

    def region(self, obj):
        return obj.tenant.region

    def grant_indefinite_lease(self, request, queryset):
        for server_lease in queryset:
            server_lease.expiry = None
            server_lease.save()
        self.message_user(
            request, f"Indefinite leases granted for {queryset.count()} server(s)"
        )

    def send_renewal_reminder_email(self, request, queryset):
        n = 0
        for server_lease in queryset:
            if server_lease.expiry:
                server_lease.send_email_renewal_reminder()
                n += 1
        self.message_user(request, f"Reminder emails sent for {n} server(s)")

    def renew_lease(self, request, queryset):
        for server_lease in queryset:
            server_lease.renew_lease()


class ServerLeaseRequestAdmin(admin.ModelAdmin):
    list_display = (
        model_str,
        "user",
        "closed",
        "granted",
        "created_at",
        "responded_at",
        "actioned_by",
    )

    readonly_fields = (
        "user",
        "server_lease",
        "created_at",
        "granted",
        "responded_at",
        "actioned_by",
    )

    ordering = ("closed", "-created_at")

    actions = ("grant_indefinite_lease_requests", "reject_indefinite_lease_requests")

    def grant_indefinite_lease_requests(self, request, queryset):
        for lease_request in queryset:
            lease_request.grant(request)
        self.message_user(
            request, f"Indefinite leases granted for {queryset.count()} server(s)"
        )

    def reject_indefinite_lease_requests(self, request, queryset):
        for lease_request in queryset:
            lease_request.reject(request)
        self.message_user(
            request, f"Indefinite leases rejected for {queryset.count()} server(s)"
        )


class RegionSettingsInline(admin.StackedInline):
    model = RegionSettings


class RegionAdmin(admin.ModelAdmin):
    inlines = (RegionSettingsInline,)


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(ServerLease, ServerLeaseAdmin)
admin.site.register(ServerLeaseRequest, ServerLeaseRequestAdmin)
