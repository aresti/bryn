import sshpubkeys

from rest_framework import serializers

from userdb.models import Region
from .models import Tenant


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name", "description", "disabled", "disable_new_instances"]


class TenantSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Tenant
        fields = ["id", "region"]


class InstanceSerializer(serializers.Serializer):
    name = serializers.RegexField(regex=r"^([a-zA-Z0-9\-]+)$", max_length=50,)
    flavor = serializers.ChoiceField(choices=[])
    image = serializers.ChoiceField(choices=[])
    key_name = serializers.ChoiceField(choices=[], required=False)
    new_key_name = serializers.RegexField(
        regex=r"^([a-zA-Z0-9\-]+)$", max_length=50, required=False
    )
    new_key = serializers.CharField(required=False)

    def validate_new_key(self, value):
        try:
            sshpubkeys.SSHKey(value).parse()
        except sshpubkeys.InvalidKeyException:
            raise serializers.ValidationError("Invalid SSH key")
        return value

    def validate(self, data):
        if not (data["key_name"] or (data["new_key_name"] and data["new_key"])):
            raise serializers.ValidationError(
                "A valid key choice, or a new name/key pair is required."
            )
        # TODO: new key name not in existing list
        return data


class ImageSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.UUIDField()
    name = serializers.CharField()


class FlavorSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.UUIDField()
    name = serializers.CharField()


class SshKeySerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    id = serializers.UUIDField()
    name = serializers.CharField()
