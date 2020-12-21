import sshpubkeys

from rest_framework import serializers

from userdb.models import Region
from . import INSTANCE_STATUS_VALUES
from .models import Tenant


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name", "description", "disabled", "disable_new_instances"]


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "region", "team"]


class OpenstackBaseSerializer(serializers.Serializer):
    team = serializers.IntegerField(required=False, allow_null=True)
    tenant = serializers.IntegerField(required=False, allow_null=True)


class InstanceSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    flavor = serializers.UUIDField()
    status = serializers.ChoiceField(choices=INSTANCE_STATUS_VALUES)
    ip = serializers.IPAddressField(read_only=True, required=False, allow_null=True)
    created = serializers.DateTimeField(read_only=True)


class ImageSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()


class FlavorSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()


class KeyPairSerializer(OpenstackBaseSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    fingerprint = serializers.CharField(read_only=True)
    public_key = serializers.CharField()

    def validate_public_key(self, value):
        try:
            sshpubkeys.SSHKey(value).parse()
        except sshpubkeys.InvalidKeyException:
            raise serializers.ValidationError("Invalid SSH key")
        return value


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
    volume_type = serializers.CharField()


class VolumeTypeSerializer(OpenstackBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    is_default = serializers.BooleanField(read_only=True, default=False)
