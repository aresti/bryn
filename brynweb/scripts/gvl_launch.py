
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
from scripts.image_launch import add_keypair

import sys
import yaml
import time

def launch_gvl(tenant, server_name, password, server_type='group'):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()

    key_name = add_keypair(nova, 'nick-key', """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQClUIKUlWckdyjIur2OhEFz4Xa2eKrpZe7ZgcVBnV3eUJi4WCPzB39aD4GvakwsUuKMGno3ipSCBI2Mcw2VfGD9oelCmPA/M6/cDvjijaQSgF5WBNoAbbaARtWyDSu+XMpbftNexmpc3CblamTm3DEgrOnhTcNJ+Imk+wBXpFUZOvfu/Ht/MBldbcgWp2RK8rgX+tCf5GUdgvA3Fz8YyvIOcIHIqSa9c9hfhes2hyLsrxe39norXUgsrgbMWlqqMYLc95TSYRFI+VYstoQ5b/6QHa/UloKkAR8LhVv8ntfRXVgvQtmUh3GzrYu326JW+kYSQ8hMX++v2w84vpL+50Rz nick@Nicks-MacBook-Pro.local""")

    #server_name = "%s-%s" % (tenant.team.name, server_type)

    user_specific_data = {'cloud_name'   : 'CLIMB',
                          'cluster_name' : server_name,
                          'key_name'     : key_name,
                          'password'     : password,
                          'freenxpass'   : password}

    tenant_id = tenant.created_tenant_id
    access, secret = client.get_ec2_keys(tenant_id)

    user_specific_data['access_key'] = access
    user_specific_data['secret_key'] = secret

    cloud_specific_data = {'ec2_conn_path'   : '/services/Cloud'}

    cloud_specific_data['cidr_range'] = client.get_cidr_range()
    cloud_specific_data['ec2_port'] = client.get_ec2_port()
    cloud_specific_data['is_secure'] = client.get_ec2_is_secure()
    cloud_specific_data['region_endpoint'] = client.get_ec2_region_endpoint()

    generic_data = """cloud_type: openstack
region_name: nova
s3_conn_path: /
s3_host: swift.rc.nectar.org.au
s3_port: 8888
bucket_default: cloudman-gvl-410
use_object_store: false
initial_cluster_type: Galaxy
galaxy_data_option: transient
gvl_config:
  install:
  - gvl_cmdline_utilities
post_start_script_url: 'file:///mnt/galaxy/gvl/poststart.d'
cluster_templates:
  - name: Galaxy
    filesystem_templates:
    - name: galaxy
      type: transient
      roles: galaxyTools,galaxyData
      data_source: archive
      archive_url: http://s3.climb.ac.uk/gvl/microgvl-fs-0.11-1-beta.tgz
      archive_md5: b116da95872802dfab5a22d8caec0f4a
    - name: gvl
      type: transient
      data_source: archive
      archive_url: http://s3.climb.ac.uk/gvl/microgvl-apps-0.11-1-beta-rebuilt.tgz
      archive_md5: 5c039ffacfe96e875c82c4bc8eb10df1
    - name: galaxyIndices
      type: transient
      roles: galaxyIndices
      archive_url: https://s3.eu-central-1.amazonaws.com/cloudman-gvl-400-frankfurt/gvl-indices-blank-4.0.0.tar.gz
      archive_md5: 09eadb352ef3be038221f4226edaadc8
  - name: Data
    filesystem_templates:
"""

#     archive_url: http://s3.climb.ac.uk/gvl/microgvl-apps-0.11-1-beta.tgz
#     archive_md5: 0c5421da6b4c432625159a9df6e12784
#     archive_url: http://s3.climb.ac.uk/gvl/microgvl-apps-0.11-1-beta-rebuilt.tgz
#     archive_md5: 5c039ffacfe96e875c82c4bc8eb10df1


    userdata = yaml.dump(user_specific_data, default_flow_style=False, allow_unicode=False) + \
                 yaml.dump(cloud_specific_data, default_flow_style=False, allow_unicode=False) + \
                 yaml.dump(yaml.load(generic_data), default_flow_style=False, allow_unicode=False)

    print userdata

    ## steps
    ## 1) find flavor
    ## 2) find network
    ## 3) allocate floating ip
    ## 4) launch

    #f = nova.floating_ips.create('public')
    #print f

    if server_type == 'group':
        fl = nova.flavors.find(name='climb.group')
    else:
        fl = nova.flavors.find(name='climb.user')

    #for i in client.get_glance().images.list():
    #    if i.name == 'GVL 4.1.0':
    #        image_id = i.id 

    #for n in nova.networks.list():
    #    print n.id, n.project_id
    #    if hasattr(n, 'tenant_id'):
    #        if n.tenant_id == default_tenant_id:
    #            print n

    cinder = client.get_cinder()

    volume = cinder.volumes.create(imageRef=tenant.region.regionsettings.gvl_image_id,
                                       name="%s %s boot volume" % (tenant.get_tenant_name(), server_name,),
                                       size=120)
    cinder.volumes.set_bootable(volume, True)

    print volume.id
    for n in xrange(20):
        v = cinder.volumes.get(volume.id)
        print v.status
        if v.status == 'available':
            break
        time.sleep(1)


#[{"boot_index": "0", "uuid": "c19be03e-07fb-4d43-8531-c0bc1f8500e6", "volume_size": "120", "source_type": "volume", "destination_type": "volume", "delete_on_termination": false}]

    bdm = [{'uuid' : volume.id, 'source_type' : 'volume', 
           'destination_type' : 'volume',
           'boot_index' : "0",
           'delete_on_termination' : True}]

    if tenant.region.name == 'warwick':
        network_id = '93ffd3af-c7cf-48d8-ba4c-ce59068c5c0a'
    else:
        network_id = tenant.created_network_id

    server = nova.servers.create(server_name,
           "",
           flavor=fl,
           nics=[{'net-id' : network_id}],
           userdata=userdata,
           key_name=key_name,
           block_device_mapping_v2=bdm)
    print server

    for n in xrange(0,20):
        server = nova.servers.get(server.id)
        print server.status

    if tenant.region.name == 'cardiff':
        f = nova.floating_ips.create('climb_external')
        server.add_floating_ip(f)
    elif tenant.region.name == 'bham':
        f = nova.floating_ips.create('public')
        server.add_floating_ip(f)

    return True

def run():
    team = Team.objects.get(pk=1)
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='bham'))[0]
    launch_gvl(tenant, 'test gvl bham', 'testtest99', 'group')
 
