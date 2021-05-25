import logging

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.core.exceptions import ImproperlyConfigured

from huey.contrib.djhuey import task
from slack import WebClient
from slack.errors import SlackApiError

logger = logging.getLogger("huey")

SLACK_ENABLED = getattr(settings, "SLACK_ENABLED", False)


@task(retries=2, retry_delay=10)
def send_mail(*args, **kwargs):
    django_send_mail(*args, **kwargs)


if SLACK_ENABLED:
    try:
        slack_token = getattr(settings, "SLACK_TOKEN")
        slack_channel = getattr(settings, "SLACK_CHANNEL")
        slack_client = WebClient(token=slack_token)
    except AttributeError:
        raise ImproperlyConfigured(
            "SLACK_CHANNEL & SLACK_TOKEN settings are required to enable Slack messages."
        )

    @task(retries=2, retry_delay=10)
    def slack_post_message(text, channel=slack_channel):
        """Post a message to slack"""
        try:
            slack_client.chat_postMessage(channel=channel, text=text)
        except SlackApiError as e:
            logger.error(f"Slack error: {e.response['error']}")


else:  # Slack disabled, print to console

    def slack_post_message(text, *args, **kwargs):
        print(text)
