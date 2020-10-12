from rest_framework import permissions
from .models import TeamMember


class IsTeamMembershipAdmin(permissions.BasePermission):
    """
    Only allow team admins.
    """

    def has_permission(self, request, view):
        """
        Check whether the current user is admin for the team.
        """
        try:
            team_id = request.resolver_match.kwargs["team_id"]
            team_member = TeamMember.objects.get(team=team_id, user=request.user)
        except TeamMember.DoesNotExist:
            return False
        return team_member.is_admin
