from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('home.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^discourse/', include('discourse.urls')),
    url(r'^reports/', include('reporting.urls')),
    url(r'^user/', include('userdb.urls')),
]
