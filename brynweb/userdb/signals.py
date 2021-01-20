from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from openstack.models import KeyPair
from .models import Invitation, Profile, Team


@receiver(post_save, sender=Invitation)
def send_invitation(sender, invitation, created, **kwargs):
    """Send an invitation email after an Invitation instance is created"""
    if not created:
        return

    context = {
        "invitation": invitation,
        "url": reverse("user:accept-invite", args=[invitation.uuid]),
    }
    subject = render_to_string("userdb/email/user_invite_subject.txt", context)
    text_content = render_to_string("userdb/email/user_invite_email.txt", context)
    html_content = render_to_string("userdb/email/user_invite_email.html", context)

    send_mail(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [invitation.email],
        html_message=html_content,
        fail_silently=False,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    profile = Profile(user=instance)
    profile.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def send_email_validation_link(sender, instance, created, **kwargs):
    """Send email validation link on profile creation"""
    if created:
        instance.send_validation_link()


@receiver(post_save, sender=Team)
def send_new_registration_admin_email(sender, instance, created, **kwargs):
    """Send email to notify admin of new registration"""
    if not (created and settings.NEW_REGISTRATION_ADMIN_EMAILS):
        return

    team = instance
    context = {"user": team.creator, "team": team}
    subject = render_to_string(
        "userdb/email/new_registration_admin_subject.txt", context
    )
    text_content = render_to_string(
        "userdb/email/new_registration_admin_email.txt", context
    )
    html_content = render_to_string(
        "userdb/email/new_registration_admin_email.html", context
    )

    send_mail(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        settings.NEW_REGISTRATION_ADMIN_EMAILS,
        html_message=html_content,
        fail_silently=True,
    )


@receiver(post_save, sender=KeyPair)
def set_first_keypair_as_default(sender, instance, created, **kwargs):
    """Set first keypair as a user's default"""
    if not created:
        return

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
