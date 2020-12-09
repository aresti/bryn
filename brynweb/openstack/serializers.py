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


class InstanceSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.UUIDField()
    name = serializers.CharField()
    flavor = serializers.UUIDField()
    status = serializers.ChoiceField(choices=INSTANCE_STATUS_VALUES)
    ip = serializers.IPAddressField(required=False, allow_null=True)
    created = serializers.DateTimeField()


class NewInstanceSerializer(serializers.Serializer):
    name = serializers.RegexField(regex=r"^([a-zA-Z0-9\-]+)$", max_length=50,)
    flavor = serializers.UUIDField()
    image = serializers.UUIDField()
    auth_key_name = serializers.RegexField(
        regex=r"^([a-zA-Z0-9\-]+)$", max_length=50, required=False
    )
    auth_key_value = serializers.CharField(required=False)

    def validate_auth_key_value(self, value):
        try:
            sshpubkeys.SSHKey(value).parse()
        except sshpubkeys.InvalidKeyException:
            raise serializers.ValidationError("Invalid SSH key")
        return value


class ImageSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.UUIDField()
    name = serializers.CharField()


class FlavorSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.UUIDField()
    name = serializers.CharField()


class KeyPairSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.CharField()
    name = serializers.CharField()
    fingerprint = serializers.CharField()
    public_key = serializers.CharField()


class VolumeAttachmentSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    attachment_id = serializers.UUIDField()
    server_id = serializers.UUIDField()
    device = serializers.CharField()
    attached_at = serializers.DateTimeField()


class VolumeSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    attachments = VolumeAttachmentSerializer(many=True)
    id = serializers.UUIDField()
    name = serializers.CharField()
    size = serializers.IntegerField()
    status = serializers.CharField()
