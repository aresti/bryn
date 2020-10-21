from rest_framework import serializers, exceptions, validators

from openstack.serializers import TenantSerializer
from .models import User, TeamMember, Invitation, Team


class TeamFromUrlDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the team identified by team_id in the resolved url.
    """

    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context["request"]
        team_id = request.resolver_match.kwargs["team_id"]
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            raise exceptions.NotFound
        return team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamMember
        fields = ["id", "user", "is_admin"]


class InvitationSerializer(serializers.ModelSerializer):
    made_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_team = serializers.HiddenField(default=TeamFromUrlDefault())

    class Meta:
        model = Invitation
        fields = ["uuid", "email", "date", "message", "made_by", "to_team"]

        # Ensure only one invite per email, per team
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Invitation.objects.all(), fields=["email", "to_team"]
            )
        ]


class TeamSerializer(serializers.ModelSerializer):
    tenants = TenantSerializer(many=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "institution",
            "department",
            "phone_number",
            "verified",
            "default_region",
            "tenants_available",
            "tenants",
        ]
