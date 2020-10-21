from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import exceptions, permissions, response, generics

from scripts.list_instances import list_instances
from userdb.permissions import IsTeamMemberPermission
from userdb.models import Team

from .models import Tenant
from .serializers import TenantSerializer


class ServiceUnavailableException(exceptions.APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


class TenantListView(generics.ListAPIView):
    """
    API list endpoint for Tenant.
    Supports 'get' action.
    Authenticated user & team admin permissions required.
    """

    serializer_class = TenantSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
    ]

    def get_queryset(self):
        """Filter by team"""
        return Tenant.objects.filter(team=self.kwargs["team_id"])


class InstanceListView(APIView):
    """
    API list endpoint for tenant instances.
    Supports 'get' action.
    Authenticated user & team member permissions required.
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
    ]

    def get(self, request, team_id, tenant_id):
        team = get_object_or_404(Team, pk=team_id)
        tenant = get_object_or_404(Tenant, pk=tenant_id, team=team)

        if tenant.region.disabled:
            raise ServiceUnavailableException

        try:
            instances = list_instances(tenant)
        except Exception:
            raise ServiceUnavailableException

        return response.Response(instances)
