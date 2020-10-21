from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
from dateutil.parser import parse as dateutilparse
from dateutil.tz import *  # noqa: F401,F403


def list_instances(tenant):
    client = OpenstackClient(
        tenant.region.name,
        username=tenant.get_auth_username(),
        password=tenant.auth_password,
        project_name=tenant.get_tenant_name(),
    )
    nova = client.get_nova()
    servers = []

    for s in nova.servers.list(detailed=True):
        ip = "unknown"
        try:
            netname = tenant.region.regionsettings.public_network_name
            ip = s.addresses[netname][0]["addr"]
        except Exception:
            ip = "unknown"

        try:
            flavor = nova.flavors.get(s.flavor["id"]).name
        except Exception:
            flavor = "unknown"

        hcreated = dateutilparse(s.created)

        servers.append(
            {
                "uuid": s.id,
                "name": s.name,
                "created": hcreated,
                "flavor": flavor,
                "status": s.status,
                "ip": ip,
                "region": tenant.region.name,
                "addresses": s.addresses,
            }
        )

    return servers


def run():
    team = Team.objects.get(pk=1)
    print(team)
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name="bham"))[0]
    print(tenant)
    list_instances(tenant)
