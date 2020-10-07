from rest_framework import permissions
from .models import TeamMember


class IsTeamMembershipAdmin(permissions.BasePermission):
    """
    Only allow team admins to edit team memberships.
    """

    def has_object_permission(self, request, view, obj):
        try:
            team_member = TeamMember.objects.get(team=obj.team, user=request.user)
        except TeamMember.DoesNotExist:
            return False
        return team_member.is_admin
