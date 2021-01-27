from django.contrib import admin
from .models import ActionLog, HypervisorStats, Tenant, Region, RegionSettings


class TenantAdmin(admin.ModelAdmin):
    pass


class ActionLogAdmin(admin.ModelAdmin):
    list_filter = ("error",)


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Region)
admin.site.register(RegionSettings)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(HypervisorStats)
