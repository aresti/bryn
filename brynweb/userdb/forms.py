from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Team


class RegistrationScreeningForm(forms.Form):
    agree_terms = forms.BooleanField(
        label="I have read and agree to the above terms and conditions", required=True
    )
    is_primary_user = forms.BooleanField(
        label="I confirm that I am the primary user for my team", required=True
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        """Modify fields without redefinition"""
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["username"].help_text = None
        self.fields[
            "password1"
        ].help_text = "8 characters or more, not too common and not entirely numeric."

    def clean_email(self):
        """
        Confirm email is unique.
        Can't enforce on a database level, since this was not set initially and several duplicates already exist.
        """
        existing = User.objects.filter(email=self.cleaned_data["email"])
        if existing.count():
            raise forms.ValidationError("A user with this email already exists.")
        else:
            return self.cleaned_data["email"]


class PrimaryUserCreationForm(CustomUserCreationForm):
    allowed_domains = ["ac.uk", "gov.uk", "nhs.uk"]

    def clean_email(self):
        """
        Confirm email is unique and part of an allowed domain.
        """
        email = self.cleaned_data["email"]

        # Check unique
        existing = User.objects.filter(email=email)
        if existing.count():
            raise forms.ValidationError("A user with this email already exists.")

        # Check domain
        domain_part = email.split("@")[-1]
        if not any(domain in domain_part for domain in self.allowed_domains):
            raise forms.ValidationError(
                f"You must use an email ending in one of: {', '.join(self.allowed_domains)}"
            )

        # Valid
        return email


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            "name",
            "institution",
            "department",
            "position",
            "phone_number",
            "research_interests",
            "intended_climb_use",
            "held_mrc_grants",
        )
        widgets = {
            "phone_number": PhoneNumberInternationalFallbackWidget,
        }
