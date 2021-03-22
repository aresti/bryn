from django.conf import settings

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .models import ServerLease


@db_periodic_task(crontab(hour="*/1"))
def send_server_lease_expiry_reminder_emails():
    """Send server lease expiry reminder emails, on specified days until expiry"""
    reminder_days = settings.SERVER_LEASE_REMINDER_DAYS
    due_leases = ServerLease.objects.active_due()
    for lease in due_leases:
        if lease.time_remaining.days in reminder_days:
            last_reminder = lease.time_since_last_reminder
            if last_reminder and lease.time_since_last_reminder.days < 1:
                continue  # Don't send reminder more than once every 24 hours
            lease.send_email_renewal_reminder()
