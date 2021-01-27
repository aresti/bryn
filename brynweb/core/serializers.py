from . import hashids
from rest_framework import exceptions, serializers


class HashidsFieldMixin:
    def to_representation(self, value):
        """Convert id to hashid"""
        rep = super().to_representation(value)
        return hashids.encode(rep)

    def to_internal_value(self, data):
        """Convert hashid to id"""
        try:
            decoded = hashids.decode(data)
        except ValueError:
            raise exceptions.NotFound
        return super().to_internal_value(decoded)


class HashidsIntegerField(HashidsFieldMixin, serializers.IntegerField):
    pass
