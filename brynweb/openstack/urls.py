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
]
