from django.urls import path

from . import views

app_name = "openstack"

urlpatterns = [
    path("tenants/", views.TenantListView.as_view(), name="api-tenant-list",),
    path("instances/", views.InstanceListView.as_view(), name="api-instance-list",),
    path(
        "instances/<uuid:instance_id>",
        views.InstanceView.as_view(),
        name="api-instance-detail",
    ),
    path(
        "instances/<uuid:instance_id>/status",
        views.InstanceStatusView.as_view(),
        name="api-instance-status",
    ),
    path("flavors/", views.FlavorListView.as_view(), name="api-flavor-list",),
    path("images/", views.ImageListView.as_view(), name="api-image-list",),
    path("keypairs/", views.KeyPairListView.as_view(), name="api-keypairs-list",),
    path(
        "keypairs/<int:tenant_id>/<str:entity_id>",
        views.KeyPairDetailView.as_view(),
        name="api-keypairs-detail",
    ),
    path("volumes/", views.VolumeListView.as_view(), name="api-volume-list"),
]
