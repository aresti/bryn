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
    pass


class ActionLogAdmin(admin.ModelAdmin):
    list_filter = ("error",)


class ServerLeaseAdmin(admin.ModelAdmin):
    list_display = (
        "server_name",
        "server_id",
        "team",
        "region",
        "last_renewed_at",
        "expiry",
        "renewal_count",
        "tenant",
        "user",
    )

    search_fields = ("server_id", "server_name")

    readonly_fields = (
        "server_id",
        "server_name",
        "last_renewed_at",
        "renewal_count",
        "tenant",
        "team",
        "region",
        "renewal_url",
    )

    actions = ("grant_perpetual_lease", "renew_lease")

    def has_add_permission(self, request):
        return False

    def team(self, obj):
        return obj.tenant.team

    def region(self, obj):
        return obj.tenant.region

    def grant_perpetual_lease(self, request, queryset):
        for server_lease in queryset:
            server_lease.expiry = None
            server_lease.save()

    def renew_lease(self, request, queryset):
        for server_lease in queryset:
            server_lease.renew_lease()


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Region)
admin.site.register(RegionSettings)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(HypervisorStats)
admin.site.register(ServerLease, ServerLeaseAdmin)
