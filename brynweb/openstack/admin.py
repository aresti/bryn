from django.contrib import admin

from .models import (
    ActionLog,
    HypervisorStats,
    Tenant,
    Region,
    RegionSettings,
    ServerLease,
)


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

    actions = ("grant_perpetual_lease", "renew_lease", "send_renewal_reminder_email")

    def has_add_permission(self, request):
        return False

    def team(self, obj):
        return obj.tenant.team

    def user(self, obj):
        return obj.assigned_teammember.user

    def region(self, obj):
        return obj.tenant.region

    def grant_perpetual_lease(self, request, queryset):
        for server_lease in queryset:
            server_lease.expiry = None
            server_lease.save()

    def send_renewal_reminder_email(self, request, queryset):
        for server_lease in queryset:
            server_lease.send_email_renewal_reminder()

    def renew_lease(self, request, queryset):
        for server_lease in queryset:
            server_lease.renew_lease()


class RegionSettingsInline(admin.StackedInline):
    model = RegionSettings


class RegionAdmin(admin.ModelAdmin):
    inlines = (RegionSettingsInline,)


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(HypervisorStats)
admin.site.register(ServerLease, ServerLeaseAdmin)
