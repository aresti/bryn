from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import generics, permissions

from .forms import CustomUserCreationForm, TeamForm, InvitationForm
from .models import Institution, Team, TeamMember, Invitation, Profile, Region
from .serializers import (
    InvitationSerializer,
    TeamSerializer,
    TeamMemberSerializer,
    UserSerializer,
)


def register(request):
    if request.method == "POST":
        userform = CustomUserCreationForm(request.POST)
        teamform = TeamForm(request.POST)

        if userform.is_valid() and teamform.is_valid():
            user = userform.save()

            profile = Profile()
            profile.current_region = Region.objects.get(name="warwick")
            profile.send_validation_link(user)

            # add team
            team = teamform.save(commit=False)
            team.creator = user
            team.verified = False
            team.default_region = Region.objects.get(name="warwick")
            team.save()

            # add team member
            member = TeamMember()
            member.team = team
            member.user = user
            member.is_admin = True
            member.save()

            messages.success(
                request,
                "Thank you for registering. Your request will be approved by "
                "an administrator and you will receive an email with further "
                "instructions",
            )

            # notify admins
            team.new_registration_admin_email()

            return HttpResponseRedirect(reverse("home:home"))
    else:
        userform = CustomUserCreationForm()
        teamform = TeamForm()

    return render(
        request, "userdb/register.html", {"userform": userform, "teamform": teamform}
    )


@login_required
def invite(request):
    if request.method == "POST":
        form = InvitationForm(request.user, request.POST)
        if form.is_valid():
            if Invitation.objects.filter(
                email=form.cleaned_data["email"], to_team=form.cleaned_data["to_team"]
            ):
                messages.error(request, "User has already been invited to this team.")
            else:
                invitation = form.save(commit=False)
                invitation.send_invitation(request.user)

                messages.success(request, "Invitation sent.")
    else:
        messages.error(request, "No information supplied for invitation")
    return HttpResponseRedirect(reverse("home:home"))


def institution_typeahead(request):
    q = request.GET.get("q", "")
    if q:
        matches = Institution.objects.filter(name__icontains=q).values_list(
            "name", flat=True
        )[:10]
    else:
        matches = Institution.objects.all().values_list("name", flat=True)
    data = list(matches)
    return JsonResponse(data, safe=False)


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


def validate_email(request, uuid):
    profile = get_object_or_404(Profile, validation_link=uuid)
    profile.email_validated = True
    profile.save()
    messages.success(
        request,
        "Thank you for confirming your email address, "
        "you can now log-in to get started.",
    )
    return HttpResponseRedirect(reverse("home:home"))


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
