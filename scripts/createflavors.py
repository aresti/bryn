import sys

from ..brynweb.openstack.client import get_nova

nova = get_nova(sys.argv[1])
print(nova.flavors.list())

nova.flavors.create(name="climb.group", ram=64 * 1024, vcpus=8, disk=120, swap=0)

nova.flavors.create(name="climb.user", ram=32 * 1024, vcpus=4, disk=120, swap=0)
