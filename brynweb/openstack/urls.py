from django.urls import path

from . import views

app_name = "openstack"

urlpatterns = [
    path(
        "teams/<int:team_id>/tenants/",
        views.TenantListView.as_view(),
        name="api-tenant-list",
    ),
    path(
        "teams/<int:team_id>/tenants/<int:tenant_id>/instances/",
        views.InstanceListView.as_view(),
        name="api-instance-list",
    ),
    path(
        "teams/<int:team_id>/tenants/<int:tenant_id>/instances/<uuid:instance_id>",
        views.InstanceView.as_view(),
        name="api-instance-detail",
    ),
    path(
        "teams/<int:team_id>/tenants/<int:tenant_id>/instances/<uuid:instance_id>/status",
        views.InstanceStatusView.as_view(),
        name="api-instance-status",
    ),
    path(
        "teams/<int:team_id>/tenants/<int:tenant_id>/flavors/",
        views.FlavorListView.as_view(),
        name="api-flavor-list",
    ),
]
