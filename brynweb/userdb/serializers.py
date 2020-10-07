from rest_framework import serializers
from .models import User, TeamMember


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamMember
        fields = ["id", "user", "is_admin"]
