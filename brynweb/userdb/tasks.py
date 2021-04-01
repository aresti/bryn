from django.conf import settings
from django.utils import timezone

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .models import Team


@db_periodic_task(crontab(hour="*/1"))
def send_team_licence_expiry_reminder_emails():
    """Send team licence expiry reminder emails, on specified days until expiry"""
    reminder_days = settings.LICENCE_RENEWAL_REMINDER_DAYS
    active_teams = Team.verified_teams.filter(licence_expiry__gte=timezone.now())
    for team in active_teams:
        time_remaining = team.licence_expiry - timezone.now()
        if time_remaining.days in reminder_days:
            last_reminder = team.licence_last_reminder_sent_at
            if last_reminder and (timezone.now() - last_reminder).days < 1:
                continue  # Don't send reminder more than once every 24 hours
            team.send_team_licence_reminder_emails()
