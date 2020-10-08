from rest_framework import permissions
from .models import TeamMember


class IsTeamMembershipAdmin(permissions.BasePermission):
    """
    Only allow team admins to edit team memberships.
    """

    def has_object_permission(self, request, view, obj):
        try:
            team_id = request.resolver_match.kwargs["team_id"]
            team_member = TeamMember.objects.get(team=team_id, user=request.user)
        except TeamMember.DoesNotExist:
            return False
        return team_member.is_admin
