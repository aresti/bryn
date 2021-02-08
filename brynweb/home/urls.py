from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.TeamDashboard.as_view(), name="home"),
    path(
        "dashboard/<path:vue_router_path>",
        views.TeamDashboard.as_view(),
        name="dashboard",
    ),
]
