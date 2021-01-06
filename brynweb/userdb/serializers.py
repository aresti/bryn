from rest_framework import serializers, validators

from openstack.serializers import TenantSerializer
from .models import User, TeamMember, Invitation, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamMember
        fields = ["id", "user", "team", "is_admin"]


class InvitationSerializer(serializers.ModelSerializer):
    made_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
    tenants = TenantSerializer(many=True, read_only=True)

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
        read_only_fields = ["id", "name", "verified", "tenants_available"]
