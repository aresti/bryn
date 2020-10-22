from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response

from novaclient import exceptions as nova_exceptions

from scripts.list_instances import list_instances
from userdb.permissions import IsTeamMemberPermission
from userdb.models import Team

from .models import Tenant
from .serializers import TenantSerializer


class ServiceUnavailable(drf_exceptions.APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


class OpenstackException(drf_exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An unexpected exception occurred."
    default_code = "openstack_exception"


class UnsupportedStateTransition(drf_exceptions.APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Unsupported state transition"
    default_code = "unsupported_state_transition"


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
            raise ServiceUnavailable

        try:
            instances = list_instances(tenant)
        except Exception as e:
            raise OpenstackException(detail=str(e))

        return Response(instances)


def get_instance(team_id, tenant_id, instance_id):
    """
    Helper function to retrieve an instance
    or raise an appropriate API exception.
    """
    tenant = get_object_or_404(Tenant, pk=tenant_id, team=team_id)

    try:
        return tenant.get_server(instance_id)
    except nova_exceptions.NotFound:
        raise drf_exceptions.NotFound
    except Exception as e:
        raise OpenstackException(detail=str(e))


class InstanceView(APIView):
    """
    API detail endpoint for instances.
    Supports 'get' and 'delete' actions.
    Authenticated user & team member permissions required.
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
    ]

    def get(self, request, team_id, tenant_id, instance_id):
        pass

    def delete(self, request, team_id, tenant_id, instance_id):
        tenant = get_object_or_404(Tenant, pk=tenant_id, team=team_id)

        try:
            tenant.terminate_server(instance_id)
            return Response(None, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise OpenstackException(detail=str(e))


class InstanceStatusView(APIView):
    """
    API endpoint for instance status.
    Supports 'get' and 'put' actions.
    Authenticated user & team member permissions required.
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeamMemberPermission,
    ]

    def get(self, request, team_id, tenant_id, instance_id):
        instance = get_instance(team_id, tenant_id, instance_id)
        return Response({"status": instance.status})

    def put(self, request, team_id, tenant_id, instance_id):
        # Get instance and tenant
        instance = get_instance(team_id, tenant_id, instance_id)
        tenant = get_object_or_404(Tenant, pk=tenant_id, team=team_id)

        # Define allowed state transitions & associated methods
        # top level is target status, 1st level is current status
        state_transitions = {
            "ACTIVE": {"ACTIVE": tenant.reboot_server, "SHUTOFF": tenant.start_server},
            "SHUTOFF": {
                "ACTIVE": tenant.stop_server,
                "SHELVED": tenant.unshelve_server,
            },
        }

        # Validate target vs current status
        target_status = request.data.status.upper()
        current_status = instance.status

        if (
            target_status not in state_transitions.keys()
            or current_status not in state_transitions[target_status].keys()
        ):
            raise UnsupportedStateTransition

        # Call transition method
        try:
            state_transitions[current_status][target_status](instance_id)
            return Response(
                {"status": get_instance(team_id, tenant_id, instance_id).status}
            )
        except Exception as e:
            raise OpenstackException(detail=str(e))
