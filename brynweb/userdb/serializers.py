from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from core.serializers import HashidsIntegerField
from openstack.serializers import TenantSerializer
from .models import Invitation, TeamMember, Team, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["default_keypair", "email_validated"]
        read_only_fields = ["email_validated"]


class UserSerializer(serializers.ModelSerializer):
    id = HashidsIntegerField(read_only=True)
    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "profile"]
        read_only_fields = ["id", "username"]

    def update(self, instance, validated_data):
        is_new_email = instance.email != validated_data.get("email", instance.email)

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

        if is_new_email:
            # Not ideal having this logic here, but since project was started without custom User model,
            # we can't just override model save()
            instance.profile.email_validated = False
            instance.profile.save()
            instance.profile.send_validation_link()

        return instance


class TeamMemberSerializer(serializers.ModelSerializer):
    id = HashidsIntegerField(read_only=True)
    team = serializers.PrimaryKeyRelatedField(
        pk_field=HashidsIntegerField(), read_only=True
    )
    user = UserSerializer()

    class Meta:
        model = TeamMember
        fields = ["id", "user", "team", "is_admin"]


class InvitationSerializer(serializers.ModelSerializer):
    to_team = serializers.PrimaryKeyRelatedField(
        pk_field=HashidsIntegerField(), read_only=True
    )
    made_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invitation
        fields = ["uuid", "email", "date", "message", "made_by", "to_team"]

    def validate(self, data):
        team = get_object_or_404(
            Team, pk=self.context["request"].resolver_match.kwargs["team_id"]
        )
        email = data["email"]
        team_users = team.users
        if Invitation.objects.filter(email=email, to_team=team, accepted=False).count():
            raise serializers.ValidationError(
                "There is already a pending invitation for this team and email address."
            )
        if team_users.filter(email=email).count():
            raise serializers.ValidationError(
                "There is already a current team member with this email address."
            )

        return data


class TeamSerializer(serializers.ModelSerializer):
    id = HashidsIntegerField(read_only=True)
    default_region = serializers.PrimaryKeyRelatedField(
        read_only=True, pk_field=HashidsIntegerField()
    )
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
