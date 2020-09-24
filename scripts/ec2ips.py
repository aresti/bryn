import sys


from ..brynweb.openstack.client import OpenstackClient

client = OpenstackClient(sys.argv[1])
sess = client.get_sess()
print(client.get_ec2_keys(sess.get_project_id()))
