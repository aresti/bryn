from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from phonenumber_field.modelfields import PhoneNumberField


class Region(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    disabled = models.BooleanField(default=False)
    disable_new_instances = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)


class Team(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Group or team name",
        help_text="e.g. Bacterial pathogenomics group",
    )
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=50, verbose_name="Position (e.g. Professor)")
    department = models.CharField(max_length=50, verbose_name="Department or Institute")
    institution = models.CharField(
        max_length=100, verbose_name="Institution (e.g. University of St. Elsewhere)"
    )
    phone_number = PhoneNumberField(max_length=20, verbose_name="Phone number")
    research_interests = models.TextField(
        verbose_name="Research interests",
        help_text="Please supply a brief synopsis of your research programme",
    )
    intended_climb_use = models.TextField(
        verbose_name="Intended use of CLIMB",
        help_text="Please let us know how you or your group intend to " "use CLIMB",
    )
    held_mrc_grants = models.TextField(
        verbose_name="Held MRC grants",
        help_text="If you currently or recent have held grant funding from "
        "the Medical Research Council it would be very helpful if you can "
        "detail it here to assist with reporting use of CLIMB",
    )
    verified = models.BooleanField(default=False)
    default_region = models.ForeignKey(
        Region, null=True, blank=True, on_delete=models.SET_NULL
    )
    tenants_available = models.BooleanField(default=False)
    users = models.ManyToManyField(User, through="TeamMember", related_name="teams")

    @property
    def admin_users(self):
        """
        Return users with admin privileges for this team (queryset)
        """
        return self.users.filter(teammember__is_admin=True)

    @property
    def regular_users(self):
        """
        Return users with regular privileges for this team (queryset)
        """
        return self.users.filter(teammember__is_admin=False)

    def new_registration_admin_email(self):
        if not settings.NEW_REGISTRATION_ADMIN_EMAILS:
            return
        context = {"user": self.creator, "team": self}
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

    def verify_and_send_notification_email(self):
        context = {"user": self.creator, "team": self}
        subject = render_to_string(
            "userdb/email/notify_team_verified_subject.txt", context
        )
        text_content = render_to_string(
            "userdb/email/notify_team_verified_email.txt", context
        )
        html_content = render_to_string(
            "userdb/email/notify_team_verified_email.html", context
        )

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [self.creator.email],
            html_message=html_content,
            fail_silently=False,
        )

        self.verified = True
        self.save()

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return "%s belongs to %s" % (self.user, self.team)


class Invitation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name="Team to invite user to",
        related_name="invitations",
    )
    made_by = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["to_team", "email"], name="unique_invitation"
            )
        ]

    def __str__(self):
        return "%s to %s" % (self.email, self.to_team)


class UserProfile(models.Model):
    validation_link = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_validated = models.BooleanField(default=False)
    current_region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def send_validation_link(self, user):
        self.user = user
        self.email_validated = False
        self.save()

        context = {
            "user": user,
            "validation_link": reverse(
                "user:validate-email", args=[self.validation_link]
            ),
        }
        subject = render_to_string(
            "userdb/email/user_verification_subject.txt", context
        )
        text_content = render_to_string(
            "userdb/email/user_verification_email.txt", context
        )
        html_content = render_to_string(
            "userdb/email/user_verification_email.html", context
        )

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content,
            fail_silently=False,
        )
