from operator import methodcaller

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from novaclient import exceptions as nova_exceptions

from scripts.list_instances import list_instances
from userdb.permissions import IsTeamMemberPermission
from .models import Tenant
from .serializers import (
    FlavorSerializer,
    ImageSerializer,
    InstanceSerializer,
    SshKeySerializer,
    TenantSerializer,
)


def get_tenants_for_user(user, tenant=None):
    """
    Return queryset for all tenant(s) owned by teams that the authenticated user is a member of.
    If tenant is specified, returns a single member queryset only if the user belongs to its team.
    """
    teams = user.teams.all()
    all_tenants = Tenant.objects.filter(team__in=teams).all()

    return all_tenants.filter(pk=tenant) if tenant else all_tenants


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
        tenant = get_object_or_404(Tenant, pk=tenant_id, team=team_id)

        if tenant.region.disabled:
            raise ServiceUnavailable

        try:
            instances = list_instances(tenant)
        except Exception as e:
            raise OpenstackException(detail=str(e))

        return Response(instances)

    def post(self, request, team_id, tenant_id):
        # Get tenant collections for choice fields
        tenant = get_object_or_404(Tenant, pk=tenant_id, team=team_id)
        try:
            key_names = tenant.get_keys()
            images = tenant.get_images()
            flavors = tenant.get_flavors()
        except Exception as e:
            raise OpenstackException(detail=str(e))
        serializer = InstanceSerializer()
        serializer.flavor.choices = flavors
        serializer.image.choices = images
        serializer.key_name.choices = key_names
        serializer.data = request.data
        serializer.is_valid()
        print(serializer.data)

        return Response(status=status.HTTP_201_CREATED)


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


class OpenstackSimpleListView(APIView):
    """
    Base class for simple openstack tenant collection views.
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    # You'll need to set these attributes on subclass
    tenant_method = None  # tenant will be passed as the first argument
    serializer_class = None  # serializer class, for response validation

    def transform_func_factory(self, tenant):
        """
        Function factory, returns a func to map openstack response to desired data structure
        Override if response differs from default [[entity1Id, entity1Name], [entity2Id, entity2Name]]
        """
        return lambda r: {"id": r[0], "name": r[1], "tenant": tenant}

    def get(self, request):
        tenants = get_tenants_for_user(request.user, request.query_params.get("tenant"))
        if not tenants:
            # no tenants for user, or no team membership for specified tenant
            return Response([])

        # query openstack api for each tenant, map response to dict
        collection = []
        for tenant in tenants:
            if tenant.region.disabled:
                continue
            try:
                response = methodcaller(self.tenant_method.__name__)(tenant)
                transform_func = self.transform_func_factory(tenant)
                data = map(transform_func, response)
                collection.extend(data)
            except Exception as e:
                raise OpenstackException(detail=str(e))

        # validate against serializer
        if collection:
            try:
                serialized = self.serializer_class(data=collection, many=True)
                serialized.is_valid()
                return Response(serialized.data)
            except Exception as e:
                raise OpenstackException(detail=str(e))

        return Response([])


class FlavorListView(OpenstackSimpleListView):
    """Flavors for tenants owned by teams that the authenticated user is a member of."""

    serializer_class = FlavorSerializer
    tenant_method = Tenant.get_flavors


class ImageListView(OpenstackSimpleListView):
    """Images for tenants owned by teams that the authenticated user is a member of."""

    serializer_class = ImageSerializer
    tenant_method = Tenant.get_images


class SshKeyListView(OpenstackSimpleListView):
    """SSH keys for tenants owned by teams that the authenticated user is a member of."""

    serializer_class = SshKeySerializer
    tenant_method = Tenant.get_keys

    def post(self, request, team_id, tenant_id):
        # TODO
        pass
