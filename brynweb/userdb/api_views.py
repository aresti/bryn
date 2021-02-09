from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import exceptions, generics, permissions

from .models import TeamMember, Invitation
from .permissions import (
    IsTeamAdminPermission,
    IsTeamAdminForUnsafePermission,
    IsTeamMemberPermission,
)
from .serializers import (
    InvitationSerializer,
    TeamSerializer,
    TeamMemberSerializer,
    UserSerializer,
)

User = get_user_model()


def get_teams_for_user(user, team=None, admin=None):
    """
    Return queryset for all teams that an authenticated user is a member of.
    If team is specified, returns a queryset with only that team, if the user is a member.
    If team & admin are specified, returns a query set with only that team, if the user is an admin.
    """
    if team:
        if admin:
            return user.teams.filter(teammember__is_admin=True)
        return user.teams.filter(pk=team)
    else:
        return user.teams.all()


class TeamDetailView(generics.RetrieveUpdateAPIView):
    """
    API detail endpoint for Team.
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
        IsTeamAdminForUnsafePermission,
    ]
    serializer_class = TeamSerializer
    lookup_url_kwarg = (
        "team_id"  # using team_id keeps view compatible with team permission classes
    )

    def get_queryset(self):
        return get_teams_for_user(self.request.user)


class TeamMemberListView(generics.ListAPIView):
    """
    API list endpoint for TeamMember.
    """

    serializer_class = TeamMemberSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
        IsTeamAdminForUnsafePermission,
    ]

    def get_queryset(self):
        team_id = self.kwargs.get("team_id")
        teams = get_teams_for_user(self.request.user, team=team_id)
        return TeamMember.objects.filter(team__in=teams)


class TeamMemberDetailView(generics.RetrieveDestroyAPIView):
    """
    API detail endpoint for TeamMember.
    """

    serializer_class = TeamMemberSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
        IsTeamAdminForUnsafePermission,
    ]

    def get_queryset(self):
        teams = get_teams_for_user(self.request.user)
        return TeamMember.objects.filter(team__in=teams)

    def delete(self, request, team_id, pk):
        if get_object_or_404(TeamMember, pk=pk).user == request.user:
            # Don't allow a team member to delete themselves
            raise exceptions.MethodNotAllowed("Own team membership cannot be deleted.")
        return super().delete(self, request, team_id, pk)


class InvitationListView(generics.ListCreateAPIView):
    """
    API list endpoint for Invitation.
    """

    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdminPermission]

    def get_queryset(self):
        team_id = self.kwargs.get("team_id")
        teams = get_teams_for_user(self.request.user, team=team_id, admin=True)
        return Invitation.objects.filter(to_team__in=teams, accepted=False)

    def perform_create(self, serializer):
        """Send email after creation"""
        invitation = serializer.save()
        invitation.send_invitation_email()


class InvitationDetailView(generics.RetrieveDestroyAPIView):
    """
    API detail endpoint for Invitation.
    """

    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdminPermission]
    queryset = Invitation.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        if self.request.method == "DELETE" and obj.accepted:
            # Don't allow accepted invitations to be deleted
            raise exceptions.MethodNotAllowed("Accepted invitations cannot be deleted.")
        return obj


class OwnUserDetailView(generics.RetrieveUpdateAPIView):
    """
    API detail endpoint for authenticated/own User.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
