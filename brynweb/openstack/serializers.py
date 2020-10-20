from rest_framework import serializers

from userdb.serializers import RegionSerializer
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Tenant
        fields = ["id", "region"]
