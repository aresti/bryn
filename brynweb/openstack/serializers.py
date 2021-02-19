from rest_framework import serializers

from core.serializers import HashidsIntegerField
from . import INSTANCE_STATUS_VALUES
from .models import KeyPair, Tenant, Region, RegionSettings, HypervisorStats


class RegionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionSettings
        fields = ["max_volume_size_gb"]
        read_only_fields = ["max_volume_size_gb"]


class RegionSerializer(serializers.ModelSerializer):
    id = HashidsIntegerField()
    settings = RegionSettingsSerializer(source="regionsettings")

    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            "description",
            "disabled",
            "disable_new_instances",
            "settings",
        ]


class TenantSerializer(serializers.ModelSerializer):
    id = HashidsIntegerField()
    team = serializers.PrimaryKeyRelatedField(
        pk_field=HashidsIntegerField(), read_only=True
    )
    region = serializers.PrimaryKeyRelatedField(
        pk_field=HashidsIntegerField(), read_only=True
    )

    class Meta:
        model = Tenant
        fields = ["id", "region", "team"]


class OpenstackBaseSerializer(serializers.Serializer):
    team = HashidsIntegerField(read_only=True)
    tenant = HashidsIntegerField(read_only=True)


class InstanceSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    flavor = serializers.UUIDField()
    image = serializers.UUIDField(required=False)
    keypair = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=INSTANCE_STATUS_VALUES, required=False)
    ip = serializers.IPAddressField(read_only=True, required=False, allow_null=True)
    created = serializers.DateTimeField(read_only=True)


class ImageSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()


class FlavorSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    ram = serializers.IntegerField()
    vcpus = serializers.IntegerField()


class KeyPairSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = KeyPair
        fields = ["id", "user", "name", "public_key", "fingerprint"]


class AttachmentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    attachment_id = serializers.UUIDField(read_only=True)
    server_id = serializers.UUIDField()
    device = serializers.CharField(read_only=True)
    attached_at = serializers.DateTimeField(read_only=True)


class VolumeSerializer(OpenstackBaseSerializer):
    attachments = AttachmentSerializer(many=True, required=False)
    bootable = serializers.BooleanField(required=False, default=False)
    created_at = serializers.DateTimeField(read_only=True)
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False, allow_null=True)
    size = serializers.IntegerField()
    status = serializers.CharField(read_only=True)
    volume_type = serializers.CharField(required=False)


class VolumeTypeSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    is_default = serializers.BooleanField(read_only=True, default=False)


class HypervisorStatsSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        pk_field=HashidsIntegerField(), read_only=True
    )

    class Meta:
        model = HypervisorStats
        exclude = ["id"]
