from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.FrontendView.as_view(), name="home"),
    path("<path:vue_router_path>", views.FrontendView.as_view(), name="home"),
]
