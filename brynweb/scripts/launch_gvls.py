from userdb.models import Team, Region
from openstack.models import get_tenant_for_team
from gvl_launch import launch_gvl


def run():
    teams = Team.objects.all()
    for t in teams:
        if t.pk >= 16 and t.pk <= 25 and t.tenants_available:
            tenant = get_tenant_for_team(t, Region.objects.get(name="warwick"))
            launch_gvl(tenant, "Your first GVL server", "climblaunchyay", "user")
