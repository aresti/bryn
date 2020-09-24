import sys

from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v2_0 import client as keystoneclient
from ..brynweb.openstack import auth_settings
from collections import defaultdict


def get_servers(region):
    authsettings = auth_settings.AUTHENTICATION[region]

    loader = loading.get_plugin_loader("password")
    auth = loader.load_from_options(
        auth_url=authsettings["AUTH_URL"],
        username=authsettings["AUTH_NAME"],
        password=authsettings["AUTH_PASSWORD"],
        project_name=authsettings["TENANT_NAME"],
    )
    sess = session.Session(auth=auth)

    nova = client.Client(2, session=sess, insecure=True)
    keystone = keystoneclient.Client(session=sess)

    search_opts = {
        "all_tenants": True,
    }

    servers = nova.servers.list(detailed=True, search_opts=search_opts)

    """tenants = {}
    for s in servers:
        if s.tenant_id not in tenants:
            tenants[s.tenant_id] = keystone.tenants.get(s.tenant_id)
        s.tenant = tenants[s.tenant_id]
    """
    users = {}
    for s in servers:
        if s.user_id not in users:
            users[s.user_id] = keystone.users.get(s.user_id)
        s.user = users[s.user_id]

    return servers


servers = get_servers(sys.argv[1])

users = defaultdict(list)

for s in servers:
    users["%s <%s>" % (s.user.name, s.user.email)].append(s)

for u, serverlist in users.iteritems():
    print("%s\n" % (u,))
    for s in serverlist:
        print(s.name)

    print

# user_id
# s, nova.flavors.get(s.flavor['id'])
#     print(nova.flavors.list())
