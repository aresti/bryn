from operator import methodcaller

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from novaclient import exceptions as nova_exceptions

from userdb.permissions import IsTeamMemberPermission
from .service import OpenstackService
from .models import Tenant
from .serializers import (
    FlavorSerializer,
    ImageSerializer,
    InstanceSerializer,
    KeyPairSerializer,
    TenantSerializer,
    VolumeSerializer,
)


class InvalidTenant(drf_exceptions.PermissionDenied):
    default_detail = (
        "The specified tenant does not exist, or user does not have team membership."
    )


def get_tenants_for_user(user, team=None, tenant=None):
    """
    Return queryset for all tenant(s) owned by teams that the authenticated user is a member of.
    If tenant is specified, returns a single member queryset only if the user belongs to its team.
    If team is specified, returns tenants owned by this team, if the user is a member.
    """
    teams = user.teams.filter(pk=team) if team else user.teams.all()
    all_tenants = Tenant.objects.filter(team__in=teams).all()

    return all_tenants.filter(pk=tenant) if tenant else all_tenants


def get_tenant_for_user(user, tenant_id):
    tenant = get_tenants_for_user(user, tenant=tenant_id).first()

    if not tenant:
        raise InvalidTenant

    if tenant.region.disabled:
        raise ServiceUnavailable

    return tenant


# TODO delete after service refactoring
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


class OpenstackAPIView(APIView):
    """
    Base class for openstack api views
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    # You'll need to set these attributes on subclass
    service = None
    serializer_class = None

    def get_transform_func(self, tenant):
        """
        Returns a func to map openstack response to desired data structure
        Override as required
        """
        return lambda r: {"id": r.id, "name": r.name, "tenant": tenant.pk}


class OpenstackRetrieveView(OpenstackAPIView):
    """
    Base class for simple openstack tenant detail views.
    """

    def get(self, request, tenant_id, entity_id):
        tenant = get_tenant_for_user(request.user, tenant_id)  # may raise
        if not entity_id:
            raise drf_exceptions.NotFound

        openstack = OpenstackService(tenant)
        try:
            response = methodcaller("get", entity_id)(
                getattr(openstack, self.service.value)
            )
            transform_func = self.get_transform_func(tenant)
            data = transform_func(response)
            serialized = self.serializer_class(data=data)
            serialized.is_valid(raise_exception=True)
        except Exception as e:
            raise OpenstackException(detail=str(e))

        return Response(serialized.data)


class OpenstackListView(OpenstackAPIView):
    """
    Base class for simple openstack tenant collection views.
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    # You'll need to set these attributes on subclass
    service = None
    serializer_class = None

    def get_transform_func(self, tenant):
        """
        Returns a func to map openstack response to desired data structure
        Override as required
        """
        return lambda r: {"id": r.id, "name": r.name, "tenant": tenant.pk}

    def get(self, request):
        query_tenant = request.query_params.get("tenant")
        query_team = request.query_params.get("team")
        tenants = get_tenants_for_user(
            request.user, tenant=query_tenant, team=query_team
        )
        if not tenants:
            # no tenants for user, or no team membership for specified tenant
            return Response([])

        # query openstack api for each tenant, map response to dict
        collection = []
        for tenant in tenants:
            if tenant.region.disabled:
                continue
            openstack = OpenstackService(tenant)
            try:
                response = methodcaller("get_list")(
                    getattr(openstack, self.service.value)
                )
                transform_func = self.get_transform_func(tenant)
                data = map(transform_func, response)
                collection.extend(data)
            except Exception as e:
                raise OpenstackException(detail=str(e))

        # validate against serializer
        if collection:
            try:
                serialized = self.serializer_class(data=collection, many=True)
                serialized.is_valid(raise_exception=True)
                return Response(serialized.data)
            except Exception as e:
                raise OpenstackException(detail=str(e))

        return Response([])


class OpenstackCreateMixin(OpenstackAPIView):
    """
    Mixin to add create/post method to openstack api views
    """

    def post(self, request):
        tenant = get_tenant_for_user(
            request.user, request.data.get("tenant")
        )  # may raise
        openstack = OpenstackService(tenant)
        try:
            serialized = self.serializer_class(data=request.data)
            serialized.is_valid(raise_exception=True)
            response = methodcaller("create", serialized.data)(
                getattr(openstack, self.service.value)
            )
        except Exception as e:
            raise OpenstackException(detail=str(e))

        transform_func = self.get_transform_func(tenant)
        return Response(transform_func(response))


class OpenstackDeleteMixin(OpenstackAPIView):
    """
    Mixin to add delete method to openstack api views
    """

    def delete(self, request, tenant_id, entity_id):
        tenant = get_tenant_for_user(request.user, tenant_id)  # may raise
        if not entity_id:
            raise drf_exceptions.NotFound

        openstack = OpenstackService(tenant)
        try:
            response = methodcaller("delete", entity_id)(
                getattr(openstack, self.service.value)
            )
            print(response)
        except Exception as e:
            raise OpenstackException(detail=str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)


class TenantListView(generics.ListAPIView):
    """
    Tenants belonging to teams that user is a member of. Accepts 'team' query parameter.
    """

    serializer_class = TenantSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return get_tenants_for_user(
            self.request.user, team=self.request.query_params.get("team")
        )


class InstanceListView(OpenstackListView):
    """
    Instances for tenants owned by teams that the authenticated user is a member of.
    """

    serializer_class = InstanceSerializer
    service = OpenstackService.Services.SERVERS

    def get_transform_func(self, tenant):
        public_netname = tenant.region.regionsettings.public_network_name
        return lambda r: {
            "id": r.id,
            "name": r.name,
            "flavor": r.flavor["id"],
            "status": r.status,
            "ip": r.addresses[public_netname][0]["addr"]
            if public_netname in r.addresses.keys()
            else None,
            "created": r.created,
            "tenant": tenant.pk,
        }

    def post(self, request, format=None):
        # Get tenant, validate team membership
        query_tenant = request.query_params.get("tenant")
        query_team = request.query_params.get("team")
        tenants = get_tenants_for_user(
            request.user, tenant=query_tenant, team=query_team
        )

        if not tenants:
            # Bad tenant id, or not a team member
            raise drf_exceptions.PermissionDenied

        tenant = tenants[0]
        # serialized = NewInstanceSerializer(data=request.data)

        print(tenant.launch_instance())
        return Response(None, status.HTTP_201_CREATED)


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


class FlavorListView(OpenstackListView):
    """
    Flavors for tenants owned by teams that the authenticated user is a member of.
    """

    serializer_class = FlavorSerializer
    service = OpenstackService.Services.FLAVORS


class ImageListView(OpenstackListView):
    """
    Images for tenants owned by teams that the authenticated user is a member of.
    """

    serializer_class = ImageSerializer
    service = OpenstackService.Services.IMAGES


def keypair_transform_func(self, tenant):
    return lambda r: {
        "id": r.id,
        "name": r.name,
        "fingerprint": r.fingerprint,
        "public_key": r.public_key,
        "tenant": tenant.pk,
    }


class KeyPairDetailView(OpenstackRetrieveView, OpenstackDeleteMixin):
    """
    SSH key pairs for tenants owned by teams that the authenticated user is a member of.
    """

    serializer_class = KeyPairSerializer
    service = OpenstackService.Services.KEYPAIRS
    get_transform_func = keypair_transform_func


class KeyPairListView(OpenstackListView, OpenstackCreateMixin):
    """
    SSH key pairs for tenants owned by teams that the authenticated user is a member of.
    """

    serializer_class = KeyPairSerializer
    service = OpenstackService.Services.KEYPAIRS
    get_transform_func = keypair_transform_func


class VolumeListView(OpenstackListView):
    """
    Volumes for tenants owned by teams that the authenticated user is a member of.
    """

    serializer_class = VolumeSerializer
    service = OpenstackService.Services.VOLUMES

    def get_transform_func(self, tenant):
        return lambda r: {
            "id": r.id,
            "attachments": r.attachments,
            "bootable": r.bootable,
            "name": r.name.replace(tenant.get_tenant_name(), "")
            if r.name
            else str(r.id),
            "size": r.size,
            "status": r.status,
            "tenant": tenant.pk,
            "volume_type": r.volume_type,
        }
