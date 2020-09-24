from ..brynweb.openstack.client import OpenstackClient, get_admin_credentials

client = OpenstackClient("warwick", **get_admin_credentials("warwick"))
glance = client.get_glance()

for i in glance.images.list():
    print(i.__dict__)
