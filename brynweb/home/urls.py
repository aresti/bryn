from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("status", views.status, name="status"),
    path("region-select", views.region_select, name="region-select"),
    path("launchcustom/<int:teamid>", views.launchcustom, name="launchcustom"),
    path("start/<int:teamid>/<uuid:uuid>", views.start, name="start"),
    path("stop/<int:teamid>/<uuid:uuid>", views.stop, name="stop"),
    path("reboot/<int:teamid>/<uuid:uuid>", views.reboot, name="reboot"),
    path("terminate/<int:teamid>/<uuid:uuid>", views.terminate, name="terminate",),
    path("unshelve/<int:teamid>/<uuid:uuid>", views.unshelve, name="unshelve"),
    path("get_instances_table", views.get_instances_table, name="get_instances_table"),
    path("", views.TeamDashboard.as_view(), name="home"),
]
