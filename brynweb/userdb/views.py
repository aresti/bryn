from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from rest_framework import generics, permissions

from .forms import (
    CustomUserCreationForm,
    PrimaryUserCreationForm,
    RegistrationScreeningForm,
    TeamForm,
)
from .models import Team, TeamMember, Invitation, Profile, Region
from .serializers import (
    InvitationSerializer,
    TeamSerializer,
    TeamMemberSerializer,
    UserSerializer,
)


# Auth views
class LoginView(auth_views.LoginView):
    template_name = "userdb/login.html"


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
            user = user_form.save()  # profile instance is created via. signal

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


class EmailValidationPendingView(TemplateView):
    """User email validation pending view"""

    template_name = "userdb/email_validation_pending.html"


class EmailValidationSendView(View):
    """User email validation send view"""

    def get(self, request):
        request.user.profile.send_validation_link()
        return HttpResponseRedirect(reverse("user:email_validation_sent"))


class EmailValidationSentView(TemplateView):
    """User email validation sent view"""

    template_name = "userdb/email_validation_sent.html"


class EmailValidationConfirmView(RedirectView):
    """Mark user profile as email validated and redirect to login"""

    pattern_name = "home:home"

    def get_redirect_url(self, *args, **kwargs):
        profile = get_object_or_404(Profile, validation_link=kwargs.pop("uuid"))
        profile.mark_email_validated()
        messages.success(self.request, "Thank you for confirming your email address.")
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


def get_teams_for_user(user, team=None):
    """
    Return queryset for all teams that an authenticated user is a member of.
    If team is specified, returns a queryset with only that team, if the user is a member.
    """
    return user.teams.filter(pk=team) if team else user.teams.all()


class IsTeamAdmin(permissions.BasePermission):
    """
    Object level permission to only allow team admins.
    Assumes the model instance is a Team object, or otherwise has a
    'team' or 'to_team' attribute.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Team):
            team = obj
        elif hasattr(obj, "to_team"):
            team = obj.to_team
        else:
            team = obj.team
        return (
            len(TeamMember.objects.filter(team=team, user=request.user, is_admin=True))
            == 1
        )


class IsTeamAdminOrReadOnly(IsTeamAdmin):
    """
    Object level permission to only allow team admins to edit/destroy.
    Assumes the model instance is a Team object, or otherwise has
    a 'team' or 'to_team' attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)


class TeamDetailView(generics.RetrieveUpdateAPIView):
    """
    API detail endpoint for Team.
    """

    permission_classes = [permissions.IsAuthenticated, IsTeamAdminOrReadOnly]
    serializer_class = TeamSerializer

    def get_queryset(self):
        return get_teams_for_user(self.request.user)


class TeamMemberListView(generics.ListAPIView):
    """
    API list endpoint for TeamMember.
    """

    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdminOrReadOnly]

    def get_queryset(self):
        query_team = self.request.query_params.get("team")
        teams = get_teams_for_user(self.request.user, team=query_team)
        return TeamMember.objects.filter(team__in=teams)


class TeamMemberDetailView(generics.RetrieveDestroyAPIView):
    """
    API detail endpoint for TeamMember.
    """

    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdmin]

    def get_queryset(self):
        teams = get_teams_for_user(self.request.user)
        return TeamMember.objects.filter(team__in=teams)


class InvitationListView(generics.ListCreateAPIView):
    """
    API list endpoint for Invitation.
    """

    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdmin]

    def get_queryset(self):
        query_team = self.request.query_params.get("team")
        teams = get_teams_for_user(self.request.user, team=query_team)
        return Invitation.objects.filter(to_team__in=teams, accepted=False)


class InvitationDetailView(generics.RetrieveDestroyAPIView):
    """
    API detail endpoint for Invitation.
    """

    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdmin]
    queryset = Invitation.objects.all()


class OwnUserDetailView(generics.RetrieveUpdateAPIView):
    """
    API detail endpoint for authenticated/own User.
    """

    serializer_class = UserSerializer
    permissions = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user
