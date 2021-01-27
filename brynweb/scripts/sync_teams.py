from userdb.models import Team
from openstack.models import get_tenant_for_team, Region
from scripts.setup_team import setup_tenant


def run():
    for t in Team.objects.all():
        for r in Region.objects.all():
            tenant = get_tenant_for_team(t, r)
            if not tenant:
                print("%s does not have %s" % (t, r))
                try:
                    setup_tenant(t, r)
                    print("success")
                except Exception as e:
                    print(e)
