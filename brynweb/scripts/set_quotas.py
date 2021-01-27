from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import get_tenant_for_team, Region
from userdb.models import Team


def set_quota(tenant):
    client = OpenstackClient(
        tenant.region.name, **get_admin_credentials(tenant.region.name)
    )

    # cinder quotas
    cinder = client.get_cinder()
    cinder.quotas.get(tenant.created_tenant_id)
    cinder.quotas.update(tenant.created_tenant_id, volumes=20, gigabytes=10000)

    # nova quotas
    nova = client.get_nova()
    nova.quotas.get(tenant.created_tenant_id)
    nova.quotas.update(tenant.created_tenant_id, cores=128, ram=650000)


def run(*args):
    region = Region.objects.get(name=args[0])
    for team in Team.objects.filter():
        tenant = get_tenant_for_team(team, region)
        if tenant:
            set_quota(tenant)
