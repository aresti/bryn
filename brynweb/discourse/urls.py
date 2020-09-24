from django.conf.urls import url
from . import views

app_name = "discourse"

urlpatterns = [
    url(r"sso", views.sso),
]
