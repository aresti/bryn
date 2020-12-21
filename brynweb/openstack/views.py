from operator import methodcaller

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response

from userdb.permissions import IsTeamMemberPermission
from .service import OpenstackService, ServiceUnavailable, OpenstackException
from .models import Tenant
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
    """
    Return a tenant for a given user, only if that user is a team member.
    """
    tenant = get_tenants_for_user(user, tenant=tenant_id).first()

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

    def get(self, request):
        query_tenant = request.query_params.get("tenant")
        query_team = request.query_params.get("team")
        tenants = get_tenants_for_user(
            request.user, tenant=query_tenant, team=query_team
        )
        if not tenants:
            # no tenants for user, or no team membership for specified tenant
            return Response([])

        # query openstack api for each tenant, transform response as required
        collection = []
        for tenant in tenants:
            if tenant.region.disabled:
                continue
            openstack = OpenstackService(tenant)
            transform_func = self.get_transform_func(tenant)
            try:
                response = methodcaller("get_list")(
                    getattr(openstack, self.service.value)
                )
                data = map(transform_func, response)
                collection.extend(data)
            except Exception as e:
                raise OpenstackException(detail=str(e))

        if collection:
            serialized = self.serializer_class(collection, many=True)
            return Response(serialized.data)
        else:
            return Response([])


class OpenstackCreateMixin(OpenstackAPIView):
    """
    Mixin to add create/post method to openstack api views.
    """

    def post(self, request):
        tenant = get_tenant_for_user(
            request.user, request.data.get("tenant")
        )  # may raise
        openstack = OpenstackService(tenant)
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

    def delete(self, request, tenant_id, entity_id):
        tenant = get_tenant_for_user(request.user, tenant_id)  # may raise
        if not entity_id:
            raise drf_exceptions.NotFound

        openstack = OpenstackService(tenant)
        try:
            methodcaller("delete", entity_id)(getattr(openstack, self.service.value))
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
            self.request.user, team=self.request.query_params.get("team")
        )


class InstanceListView(OpenstackListView):
    """
    Instance list view.
    """

    serializer_class = InstanceSerializer
    service = OpenstackService.Services.SERVERS

    def get_transform_func(self, tenant):
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


# class InstanceStatusView(APIView):
#     """
#     API endpoint for instance status.
#     Supports 'get' and 'put' actions.
#     Authenticated user & team member permissions required.
#     """

#     permission_classes = [
#         permissions.IsAuthenticated,
#         IsTeamMemberPermission,
#     ]

#     def get(self, request, team_id, tenant_id, instance_id):
#         instance = get_instance(team_id, tenant_id, instance_id)
#         return Response({"status": instance.status})

#     def put(self, request, team_id, tenant_id, instance_id):
#         # Get instance and tenant
#         instance = get_instance(team_id, tenant_id, instance_id)
#         tenant = get_object_or_404(Tenant, pk=tenant_id, team=team_id)

#         # Define allowed state transitions & associated methods
#         # top level is target status, 1st level is current status
#         state_transitions = {
#             "ACTIVE": {"ACTIVE": tenant.reboot_server, "SHUTOFF": tenant.start_server},
#             "SHUTOFF": {
#                 "ACTIVE": tenant.stop_server,
#                 "SHELVED": tenant.unshelve_server,
#             },
#         }

#         # Validate target vs current status
#         target_status = request.data.status.upper()
#         current_status = instance.status

#         if (
#             target_status not in state_transitions.keys()
#             or current_status not in state_transitions[target_status].keys()
#         ):
#             raise UnsupportedStateTransition

#         # Call transition method
#         try:
#             state_transitions[current_status][target_status](instance_id)
#             return Response(
#                 {"status": get_instance(team_id, tenant_id, instance_id).status}
#             )
#         except Exception as e:
#             raise OpenstackException(detail=str(e))


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


class KeyPairDetailView(OpenstackRetrieveView, OpenstackDeleteMixin):
    """
    SSH key pair detail view.
    """

    serializer_class = KeyPairSerializer
    service = OpenstackService.Services.KEYPAIRS


class KeyPairListView(OpenstackListView, OpenstackCreateMixin):
    """
    SSH key pair list view.
    """

    serializer_class = KeyPairSerializer
    service = OpenstackService.Services.KEYPAIRS


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

    def patch(self, request, tenant_id, entity_id):
        tenant = get_tenant_for_user(request.user, tenant_id)  # may raise
        if not entity_id:
            raise drf_exceptions.NotFound

        openstack = OpenstackService(tenant)
        service = getattr(openstack, self.service.value)
        attachments = request.data.get("attachments")
        try:
            if attachments is not None and len(attachments) == 0:
                # Detach
                methodcaller("detach", entity_id)(service)
            elif attachments:
                # Create attachment
                serialized_attachment = AttachmentSerializer(attachments[0])
                methodcaller(
                    "attach", entity_id, serialized_attachment.data["server_id"]
                )(service)
        except Exception as e:
            if getattr(e, "code", None) == 404 == 404:
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
