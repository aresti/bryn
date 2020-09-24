import sys


from ..brynweb.openstack.client import get_nova

nova = get_nova(sys.argv[1])
fl = nova.flavors.find(name="climb.group")

# destroy all servers
for s in nova.servers.list(search_opts={"flavor": fl.id}):
    print("deleting %s" % (s,))
    nova.servers.delete(s)
