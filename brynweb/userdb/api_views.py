from django.contrib.auth import get_user_model

from rest_framework import generics, permissions

from .models import Team, TeamMember, Invitation
from .serializers import (
    InvitationSerializer,
    TeamSerializer,
    TeamMemberSerializer,
    UserSerializer,
)

User = get_user_model()


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
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user