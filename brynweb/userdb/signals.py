from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from openstack.models import KeyPair
from .models import Invitation


@receiver(post_save, sender=Invitation)
def send_invitation(sender, instance, created, **kwargs):
    """Send an invitation email after an Invitation instance is created"""
    if not created:
        pass

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


@receiver(post_save, sender=KeyPair)
def set_first_keypair_as_default(sender, instance, created, **kwargs):
    """Set first keypair as a user's default"""
    if not created:
        pass

    if KeyPair.objects.filter(user=instance.user).count() == 1:
        # Set first keypair as the user default
        profile = instance.user.profile
        profile.default_keypair = instance
        profile.save()


@receiver(post_delete, sender=KeyPair)
def replace_default_keypair_on_deletion(sender, instance, **kwargs):
    """Assign a new default for the user, if the current one is deleted"""
    user = instance.user
    profile = user.profile
    remaining_keypairs = user.keypairs
    if profile.default_keypair is None and remaining_keypairs.count():
        profile.default_keypair = remaining_keypairs.first()
        profile.save()
