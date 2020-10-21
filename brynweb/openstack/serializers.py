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
