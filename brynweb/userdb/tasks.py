import logging

from django.conf import settings
from django.utils import timezone

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from core.utils import slack_post_templated_message
from .models import Team

logger = logging.getLogger("huey")


def send_team_licence_expiry_reminder_emails():
    """Send team licence expiry reminder emails, on specified days until expiry"""
    reminder_days = settings.LICENCE_RENEWAL_REMINDER_DAYS
    licenced_teams = Team.objects.licence_valid()
    sent_count = 0
    for team in licenced_teams:
        time_remaining = team.licence_expiry - timezone.now()
        if time_remaining.days in reminder_days:
            last_reminder = team.licence_last_reminder_sent_at
            if last_reminder and (timezone.now() - last_reminder).days < 1:
                continue  # Don't send reminder more than once every 24 hours
            team.send_team_licence_reminder_emails()
            logger.info(
                f"Sent licence renewal reminder emails for team '{team.name}' with {time_remaining.days} days until "
                "expiry"
            )
            sent_count += 1

    # Slack notification
    if sent_count:
        slack_template = "userdb/slack/sent_team_licence_renewal_reminder_emails.txt"
        slack_post_templated_message(slack_template, {"sent_count": sent_count})


if getattr(settings, "LICENCE_RENEWAL_SCHEDULED_EMAILS", False):
    db_periodic_task(crontab(minute="0", hour="10,15"))(
        send_team_licence_expiry_reminder_emails
    )
