from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from .forms import (
    CustomAuthenticationForm,
    CustomSetPasswordForm,
    CustomUserCreationForm,
    PrimaryUserCreationForm,
    RegistrationScreeningForm,
    TeamForm,
)
from .models import TeamMember, Invitation, Profile, Region
from .tokens import account_activation_token

User = get_user_model()


# Auth views
class LoginView(auth_views.LoginView):
    template_name = "userdb/login.html"
    form_class = CustomAuthenticationForm


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "userdb/password_reset_form.html"
    email_template_name = "userdb/email/password_reset_email.txt"
    html_email_template_name = "userdb/email/password_reset_email.html"
    subject_template_name = "userdb/email/password_reset_subject.txt"
    success_url = reverse_lazy("user:password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "userdb/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "userdb/password_reset_confirm.html"
    success_url = reverse_lazy("user:password_reset_complete")
    form_class = CustomSetPasswordForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "userdb/password_reset_complete.html"


class RegistrationScreeningView(FormView):
    """Registration screening view"""

    template_name = "userdb/register.html"
    form_class = RegistrationScreeningForm
    success_url = reverse_lazy("user:register_team")


def team_registration_view(request):
    """Team registration form view"""

    if request.method == "POST":
        user_form = PrimaryUserCreationForm(request.POST)
        team_form = TeamForm(request.POST)

        if user_form.is_valid() and team_form.is_valid():
            user = user_form.save(
                commit=False
            )  # profile instance is created via. signal
            user.is_active = False  # pending email validation
            user.save()

            # create team
            team = team_form.save(commit=False)
            team.creator = user
            team.save()

            # create team member
            member = TeamMember(team=team, user=user, is_admin=True)
            member.save()

            return HttpResponseRedirect(reverse("user:register_team_done"))
    else:
        user_form = CustomUserCreationForm()
        team_form = TeamForm()

    return render(
        request,
        "userdb/register_team.html",
        {"user_form": user_form, "team_form": team_form},
    )


class TeamRegistrationDoneView(TemplateView):
    """Team registration done view"""

    template_name = "userdb/register_team_done.html"


class EmailValidationSentView(TemplateView):
    """User email validation sent view"""

    template_name = "userdb/email_validation_sent.html"


class EmailValidationConfirmView(RedirectView):
    """Mark user profile as email validated and redirect to login"""

    pattern_name = "home:home"

    def get_redirect_url(self, *args, **kwargs):
        """Check activation token"""
        try:
            user_id = urlsafe_base64_decode(kwargs.pop("uidb64"))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Http404

        if account_activation_token.check_token(user, kwargs.pop("token")):
            user.profile.mark_email_validated()
            messages.success(
                self.request, "Thank you for confirming your email address."
            )
        else:
            messages.error(
                "Account activation link has expired. We've sent you a new one!"
            )
            user.profile.send_validation_link()

        return super().get_redirect_url(*args, **kwargs)


def accept_invite(request, uuid):
    i = get_object_or_404(Invitation, uuid=uuid)
    if request.method == "POST":
        userform = CustomUserCreationForm(request.POST)
        if userform.is_valid():
            user = userform.save()

            # add user profile
            profile = Profile()
            profile.user = user
            profile.current_region = Region.objects.get(name="warwick")
            profile.email_validated = True
            profile.save()

            # add team member
            member = TeamMember()
            member.team = i.to_team
            member.user = user
            member.is_admin = False
            member.save()

            i.accepted = True
            i.save()

            messages.success(
                request,
                "Congratulations you are now a member of %s. "
                "Please log-in to get started." % (member.team),
            )
            return HttpResponseRedirect(reverse("home:home"))
        else:
            messages.error(request, "Invalid values supplied for form.")
    else:
        i = Invitation.objects.get(uuid=uuid)
        if i.accepted:
            messages.error(request, "This invitation has already been claimed!")
            return HttpResponseRedirect(reverse("home:home"))

        userform = CustomUserCreationForm()
        userform.initial["email"] = i.email

    return render(request, "userdb/user-register.html", {"form": userform})
