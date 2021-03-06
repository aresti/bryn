import logging

from django.conf import settings
from django.utils import timezone

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from core.utils import slack_post_templated_message
from .models import HypervisorStats, Region, ServerLease
from .service import OpenstackService

logger = logging.getLogger("huey")


def update_hypervisor_stats():
    for region in Region.objects.filter(disabled=False):
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
        logger.info(f"Updated Hypervisor Stats for {region.name}")


if getattr(settings, "POLL_FOR_HYPERVISOR_STATS", False):
    db_periodic_task(crontab(minute="10", hour="*/1"))(update_hypervisor_stats)


def send_server_lease_expiry_reminder_emails():
    """Send server lease expiry reminder emails, on specified days until expiry"""
    reminder_days = settings.SERVER_LEASE_REMINDER_DAYS
    due_leases = ServerLease.objects.active_due()
    sent_count = 0
    for lease in due_leases:
        if lease.time_remaining.days in reminder_days:
            last_reminder = lease.last_reminder_sent_at
            if last_reminder and (timezone.now() - last_reminder).days < 1:
                continue  # Don't send reminder more than once every 24 hours
            lease.send_email_renewal_reminder()
            logger.info(
                f"Sent server lease expiry reminder for '{lease.server_name}' to {lease.assigned_teammember.user.email}"
            )
            sent_count += 1

    # Slack notification
    if sent_count:
        slack_template = "openstack/slack/sent_server_lease_reminder_emails.txt"
        slack_post_templated_message(slack_template, {"sent_count": sent_count})


if getattr(settings, "SERVER_LEASE_SCHEDULED_EMAILS", False):
    db_periodic_task(crontab(minute="0", hour="9,14"))(
        send_server_lease_expiry_reminder_emails
    )
