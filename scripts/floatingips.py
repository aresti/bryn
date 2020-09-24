import sys

from ..brynweb.openstack.client import get_nova

nova = get_nova(sys.argv[1])

f = nova.floating_ips.create("public")
print(f)

for f in nova.floating_ips.list():
    print(f)
