from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Invitation


@receiver(post_save, sender=Invitation)
def send_invitation(sender, instance, created, **kwargs):
    context = {
        "invitation": instance,
        "url": reverse("user:accept-invite", args=[instance.uuid]),
    }
    subject = render_to_string("userdb/email/user_invite_subject.txt", context)
    text_content = render_to_string("userdb/email/user_invite_email.txt", context)
    html_content = render_to_string("userdb/email/user_invite_email.html", context)

    send_mail(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email],
        html_message=html_content,
        fail_silently=False,
    )
