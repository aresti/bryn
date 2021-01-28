from django.urls import path

from openstack import api_views as openstack_views
from userdb import api_views as userdb_views

app_name = "api"

urlpatterns = [
    #  Openstack
    path("tenants/", openstack_views.TenantListView.as_view(), name="tenants",),
    path("instances/", openstack_views.InstanceListView.as_view(), name="instances",),
    path(
        "instances/<int:tenant_id>/<str:entity_id>",
        openstack_views.InstanceDetailView.as_view(),
        name="instances",
    ),
    path("flavors/", openstack_views.FlavorListView.as_view(), name="flavors",),
    path("images/", openstack_views.ImageListView.as_view(), name="images",),
    path("keypairs/", openstack_views.KeyPairListView.as_view(), name="keypairs",),
    path(
        "keypairs/<uuid:pk>",
        openstack_views.KeyPairDetailView.as_view(),
        name="keypairs",
    ),
    path("volumes/", openstack_views.VolumeListView.as_view(), name="volumes"),
    path(
        "volumes/<int:tenant_id>/<str:entity_id>",
        openstack_views.VolumeDetailView.as_view(),
        name="volumes",
    ),
    path(
        "volumetypes/", openstack_views.VolumeTypeListView.as_view(), name="volumetypes"
    ),
    # Userdb routes
    # {% url "api:team" team_id=team.id %}
    path(
        "teams/<hashids:team_id>", userdb_views.TeamDetailView.as_view(), name="teams",
    ),
    # {% url "api:team_members" team_id=team.id%}
    path(
        "teams/<hashids:team_id>/members/",
        userdb_views.TeamMemberListView.as_view(),
        name="team_members",
    ),
    # {% url "api:team_members" team_id=team.id pk=teammember.pk %}
    path(
        "teams/<hashids:team_id>/members/<hashids:pk>",
        userdb_views.TeamMemberDetailView.as_view(),
        name="team_members",
    ),
    # {% url "api:invitations" team_id=team.id %}
    path(
        "teams/<hashids:team_id>/invitations/",
        userdb_views.InvitationListView.as_view(),
        name="invitations",
    ),
    # {% url "api:invitations" team_id=team.id pk=invitation.pk %}
    path(
        "teams/<hashids:team_id>/invitations/<uuid:pk>",
        userdb_views.InvitationDetailView.as_view(),
        name="invitations",
    ),
    # {% url "api:userprofile" %}
    path(
        "userprofile/", userdb_views.OwnUserDetailView.as_view(), name="user_profile",
    ),
]
