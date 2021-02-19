from openstack.models import HypervisorStats, Region
from openstack.service import OpenstackService


def run():
    for region in Region.objects.all():
        if not region.disabled:
            service = OpenstackService(region=region)
            stats = service.nova.hypervisors.statistics()
            defaults = {
                "hypervisor_count": stats.count,
                "disk_available_least": stats.disk_available_least,
                "free_disk_gb": stats.free_disk_gb,
                "free_ram_mb": stats.free_ram_mb,
                "local_gb": stats.local_gb,
                "local_gb_used": stats.local_gb_used,
                "memory_mb": stats.memory_mb,
                "memory_mb_used": stats.memory_mb_used,
                "running_vms": stats.running_vms,
                "vcpus": stats.vcpus,
                "vcpus_used": stats.vcpus_used,
            }
            HypervisorStats.objects.update_or_create(defaults=defaults, region=region)
