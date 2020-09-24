from django.shortcuts import render
from openstack.client import OpenstackClient


def index(request):
    client = OpenstackClient(request.GET.get("region", "bham"))
    servers = client.get_servers()
    context = {"servers": servers}
    return render(request, "reporting/servers.html", context)
