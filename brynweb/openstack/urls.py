from django.urls import path

from . import views

app_name = "openstack"

urlpatterns = [
    path("tenants/", views.TenantListView.as_view(), name="api-tenant-list",),
    path("instances/", views.InstanceListView.as_view(), name="api-instance-list",),
    path(
        "instances/<int:tenant_id>/<str:entity_id>",
        views.InstanceDetailView.as_view(),
        name="api-instance-detail",
    ),
    path("flavors/", views.FlavorListView.as_view(), name="api-flavor-list",),
    path("images/", views.ImageListView.as_view(), name="api-image-list",),
    path("keypairs/", views.KeyPairListView.as_view(), name="api-keypair-list",),
    path(
        "keypairs/<int:tenant_id>/<str:entity_id>",
        views.KeyPairDetailView.as_view(),
        name="api-keypair-detail",
    ),
    path("volumes/", views.VolumeListView.as_view(), name="api-volume-list"),
    path(
        "volumes/<int:tenant_id>/<str:entity_id>",
        views.VolumeDetailView.as_view(),
        name="api-volume-detail",
    ),
    path(
        "volumetypes/", views.VolumeTypeListView.as_view(), name="api-volumetype-list"
    ),
]
