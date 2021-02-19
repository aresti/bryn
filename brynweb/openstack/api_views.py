from operator import methodcaller

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response

from .service import OpenstackService, ServiceUnavailable, OpenstackException
from .models import Tenant, KeyPair
from .serializers import (
    AttachmentSerializer,
    FlavorSerializer,
    ImageSerializer,
    InstanceSerializer,
    KeyPairSerializer,
    TenantSerializer,
    VolumeSerializer,
    VolumeTypeSerializer,
)

User = get_user_model()


class InvalidTenant(drf_exceptions.PermissionDenied):
    default_detail = (
        "The specified tenant does not exist, or user does not have team membership."
    )


def get_tenants_for_user(
    user: User, team_id: int = None, tenant_id: int = None
) -> QuerySet:
    """
    Return queryset for all tenant(s) owned by teams that the authenticated user is a member of.
    If tenant_id is specified: returns a single member queryset (only if the user is a team member).
    If team_id is specified: returns tenants belonging to this team (only if the user is a team member)
    """
    teams = user.teams.filter(pk=team_id) if team_id else user.teams.all()
    all_tenants = Tenant.objects.filter(team__in=teams).all()
    return all_tenants.filter(pk=tenant_id) if tenant_id else all_tenants


def get_tenant_for_user(user: User, tenant_id: int, team_id: int = None) -> Tenant:
    """
    Return a tenant for a given user, only if that user is a team member.
    If team_id is specified: will raise if the specified tenant does not belong to this team.
    """
    tenant = get_tenants_for_user(user, tenant_id=tenant_id, team_id=team_id).first()

    if not tenant:
        raise InvalidTenant

    if tenant.region.disabled:
        raise ServiceUnavailable

    return tenant


class OpenstackAPIView(APIView):
    """
    Base class for openstack api views.
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    # You'll need to set these attributes on subclass
    service = None
    serializer_class = None

    def get_transform_func(self, tenant):
        """
        Returns a func to map openstack response to required serializer data structure
        Override as required
        """

        def transform_func(obj):
            obj.tenant = tenant.pk
            obj.team = tenant.team.pk
            return obj

        return transform_func


class OpenstackRetrieveView(OpenstackAPIView):
    """
    Base class for simple openstack detail views.
    """

    def get(self, request, team_id, tenant_id, pk):
        tenant = get_tenant_for_user(
            request.user, tenant_id=tenant_id, team_id=team_id
        )  # may raise

        openstack = OpenstackService(tenant=tenant)
        transform_func = self.get_transform_func(tenant)
        try:
            response = methodcaller("get", pk)(getattr(openstack, self.service.value))
            data = transform_func(response)
            serialized = self.serializer_class(data)
        except Exception as e:
            if getattr(e, "code", None) == 404:
                raise drf_exceptions.NotFound
            raise OpenstackException(detail=str(e))

        return Response(serialized.data)


class OpenstackListView(OpenstackAPIView):
    """
    Base class for simple openstack collection views.
    """

    def get(self, request, team_id, tenant_id):
        tenant = get_tenant_for_user(
            request.user, team_id=team_id, tenant_id=tenant_id
        )  # may raise

        openstack = OpenstackService(tenant=tenant)
        transform_func = self.get_transform_func(tenant)
        try:
            response = methodcaller("get_list")(getattr(openstack, self.service.value))
            data = map(transform_func, response)
            serialized = self.serializer_class(data, many=True)
        except Exception as e:
            raise OpenstackException(detail=str(e))

        return Response(serialized.data)


class OpenstackCreateMixin(OpenstackAPIView):
    """
    Mixin to add create/post method to openstack api views.
    """

    def post(self, request, team_id, tenant_id):
        tenant = get_tenant_for_user(
            request.user, team_id=team_id, tenant_id=tenant_id
        )  # may raise
        openstack = OpenstackService(tenant=tenant)
        transform_func = self.get_transform_func(tenant)

        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)

        try:
            response = methodcaller("create", serialized.data)(
                getattr(openstack, self.service.value)
            )
            transformed_response = transform_func(response)
            return Response(self.serializer_class(transformed_response).data)
        except Exception as e:
            raise OpenstackException(detail=str(e))


class OpenstackDeleteMixin(OpenstackAPIView):
    """
    Mixin to add delete method to openstack api views.
    """

    def delete(self, request, team_id, tenant_id, pk):
        tenant = get_tenant_for_user(
            request.user, team_id=team_id, tenant_id=tenant_id
        )  # may raise

        openstack = OpenstackService(tenant=tenant)
        try:
            methodcaller("delete", pk)(getattr(openstack, self.service.value))
        except Exception as e:
            if getattr(e, "code", None) == 404:
                raise drf_exceptions.NotFound
            raise OpenstackException(detail=str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)


class TenantListView(generics.ListAPIView):
    """
    Tenant list view.
    """

    serializer_class = TenantSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return get_tenants_for_user(
            self.request.user, team_id=self.kwargs.get("team_id")
        )


def get_instance_transform_func(self, tenant):
    """
    Transform function factory for Instance views
    """
    public_netname = tenant.region.regionsettings.public_network_name

    def transform_func(obj):
        obj.tenant = tenant.pk
        obj.team = tenant.team.pk
        obj.flavor = obj.flavor["id"]

        if public_netname in obj.addresses.keys():
            obj.ip = obj.addresses[public_netname][0]["addr"]
        else:
            obj.ip = None

        return obj

    return transform_func


class InstanceListView(OpenstackListView, OpenstackCreateMixin):
    """
    Instance list view.
    """

    serializer_class = InstanceSerializer
    service = OpenstackService.Services.SERVERS
    get_transform_func = get_instance_transform_func


class InstanceDetailView(OpenstackRetrieveView, OpenstackDeleteMixin):
    """
    Instance detail view.
    """

    serializer_class = InstanceSerializer
    service = OpenstackService.Services.SERVERS
    get_transform_func = get_instance_transform_func

    # Define allowed state transitions & associated method names
    # top level is current status, 1st level is target status
    state_transitions = {
        "ACTIVE": {"ACTIVE": "reboot", "SHUTOFF": "stop"},
        "SHUTOFF": {"ACTIVE": "start"},
        "SHELVED": {"SHUTOFF": "unshelve"},
    }

    def patch(self, request, team_id, tenant_id, pk):
        tenant = get_tenant_for_user(
            request.user, team_id=team_id, tenant_id=tenant_id
        )  # may raise

        openstack = OpenstackService(tenant=tenant)
        service = getattr(openstack, self.service.value)

        target_status = request.data.get("status")
        if not target_status:
            raise drf_exceptions.BadRequest

        try:
            server = service.get(pk)
            current_status = server.status
            method_name = self.state_transitions[current_status][target_status]
            methodcaller(method_name, server)(service)
        except Exception as e:
            if getattr(e, "code", None) == 404:
                raise drf_exceptions.NotFound
            raise OpenstackException(detail=str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)


class FlavorListView(OpenstackListView):
    """
    Flavor list view.
    """

    serializer_class = FlavorSerializer
    service = OpenstackService.Services.FLAVORS


class ImageListView(OpenstackListView):
    """
    Image list view.
    """

    serializer_class = ImageSerializer
    service = OpenstackService.Services.IMAGES


class KeyPairListView(generics.ListCreateAPIView):
    """
    SSH key pair list view.
    """

    serializer_class = KeyPairSerializer

    def get_queryset(self):
        user = self.request.user
        return user.keypairs.all()


class KeyPairDetailView(generics.RetrieveDestroyAPIView):
    """
    SSH key pair detail view.
    """

    serializer_class = KeyPairSerializer
    queryset = KeyPair.objects.all()


def get_volume_transform_func(self, tenant):
    """
    Transform function factory for Volume views
    """

    def transform_func(obj):
        as_dict = obj.to_dict()
        as_dict["tenant"] = tenant.pk
        as_dict["team"] = tenant.team.pk
        as_dict["name"] = (
            obj.name.replace(tenant.get_tenant_name(), "") if obj.name else str(obj.id)
        )
        return as_dict

    return transform_func


class VolumeDetailView(OpenstackRetrieveView, OpenstackDeleteMixin):
    """
    Volume detail view.
    """

    serializer_class = VolumeSerializer
    service = OpenstackService.Services.VOLUMES
    get_transform_func = get_volume_transform_func

    def patch(self, request, team_id, tenant_id, pk):
        tenant = get_tenant_for_user(
            request.user, team_id=team_id, tenant_id=tenant_id
        )  # may raise

        openstack = OpenstackService(tenant=tenant)
        service = getattr(openstack, self.service.value)
        attachments = request.data.get("attachments")
        try:
            if attachments is not None and len(attachments) == 0:
                # Detach
                methodcaller("detach", pk)(service)
            elif attachments:
                # Create attachment
                serialized_attachment = AttachmentSerializer(attachments[0])
                methodcaller("attach", pk, serialized_attachment.data["server_id"])(
                    service
                )
        except Exception as e:
            if getattr(e, "code", None) == 404:
                raise drf_exceptions.NotFound
            raise OpenstackException(detail=str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)


class VolumeListView(OpenstackListView, OpenstackCreateMixin):
    """
    Volume list view.
    """

    serializer_class = VolumeSerializer
    service = OpenstackService.Services.VOLUMES
    get_transform_func = get_volume_transform_func


class VolumeTypeListView(OpenstackListView):
    """
    Volume type list view.
    """

    serializer_class = VolumeTypeSerializer
    service = OpenstackService.Services.VOLUME_TYPES
