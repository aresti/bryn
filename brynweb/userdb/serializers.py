from rest_framework import serializers, validators
from django.contrib.auth import get_user_model

from openstack.serializers import TenantSerializer
from .models import Invitation, TeamMember, Team, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["default_keypair", "email_validated"]
        read_only_fields = ["email_validated"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "profile"]
        read_only_fields = ["id", "username"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        profile_data = validated_data.get("profile", None)
        if profile_data:
            profile = instance.profile
            profile.default_keypair = profile_data.get(
                "default_keypair", profile.default_keypair
            )
            profile.save()

        return instance


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
