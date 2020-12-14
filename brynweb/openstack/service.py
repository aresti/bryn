from enum import Enum

from openstack.client import OpenstackClient


class OpenstackService:
    class Services(Enum):
        KEYPAIRS = "keypairs"
        SERVERS = "servers"
        VOLUMES = "volumes"
        FLAVORS = "flavors"
        IMAGES = "images"

    def __init__(self, tenant):
        self.tenant = tenant

        self._client = None
        self._nova = None
        self._cinder = None
        self._glance = None

        self.keypairs = KeypairsService(self)
        self.servers = ServersService(self)
        self.volumes = VolumesService(self)
        self.flavors = FlavorsService(self)
        self.images = ImagesService(self)

    @property
    def client(self):
        if not self._client:
            self._client = OpenstackClient(
                self.tenant.region.name,
                username=self.tenant.get_tenant_name(),
                password=self.tenant.auth_password,
                project_name=self.tenant.get_tenant_name(),
            )
        return self._client

    @property
    def nova(self):
        if not self._nova:
            self._nova = self.client.get_nova()
        return self._nova

    @property
    def cinder(self):
        if not self._cinder:
            self._cinder = self.client.get_cinder()
        return self._cinder

    @property
    def glance(self):
        if not self._glance:
            self._glance = self.client.get_glance()
        return self._glance


class KeypairsService:
    def __init__(self, openstack):
        self.openstack = openstack

    @property
    def nova(self):
        return self.openstack.nova

    def create(self, data):
        return self.nova.keypairs.create(
            name=data.get("name"), public_key=data.get("public_key")
        )

    def get(self, keypair_id):
        return self.nova.keypairs.get(keypair_id)

    def get_list(self):
        return self.nova.keypairs.list()

    def delete(self, keypair_id):
        keypair = self.get(keypair_id)
        keypair.delete()


class ImagesService:
    def __init__(self, openstack):
        self.openstack = openstack

    @property
    def glance(self):
        return self.openstack.glance

    def get_list(self):
        return self.glance.images.list()


class FlavorsService:
    def __init__(self, openstack):
        self.openstack = openstack

    @property
    def nova(self):
        return self.openstack.nova

    def get_list(self):
        return self.nova.flavors.list()


class VolumesService:
    def __init__(self, openstack):
        self.openstack = openstack

    @property
    def cinder(self):
        return self.openstack.cinder

    def get_list(self):
        return self.cinder.volumes.list()


class ServersService:
    def __init__(self, openstack):
        self.openstack = openstack

    @property
    def nova(self):
        return self.openstack.nova

    def get(self, uuid):
        return self.nova.servers.get(uuid)

    def get_list(self):
        return self.nova.servers.list(detailed=True)

    def start(self, uuid):
        server = self.get(uuid)
        server.start()

    def stop(self, uuid):
        server = self.get(uuid)
        server.stop()

    def terminate(self, uuid):
        server = self.get(uuid)
        server.delete()

    def unshelve(self, uuid):
        server = self.get(uuid)
        server.unshelve()

    def reboot(self, uuid):
        server = self.get(uuid)
        server.reboot(reboot_type="HARD")

    def launch(self, name, flavor, image, auth_key_name, auth_key_value=None):
        # client = self.get_client()

        # Create boot volume, wait for it to become available
        # cinder = client.get_cinder()
        # volume = cinder.volumes.create(
        #     imageRef=image,
        #     name=f"{self.get_tenant_name()} {name} boot volume",
        #     size=120,
        # )
        # cinder.volumes.set_bootable(volume, True)

        # for n in range(20):
        #     # TODO find a better way!
        #     v = cinder.volumes.get(volume.id)
        #     if v.status == "available":
        #         break
        #     time.sleep(1)

        # bdm = [
        #     {
        #         "uuid": volume.id,
        #         "source_type": "volume",
        #         "destination_type": "volume",
        #         "boot_index": "0",
        #         "delete_on_termination": True,
        #     }
        # ]

        net_id = self.get_network_id()

        print(name)
        print(flavor)
        print(net_id)
        print(auth_key_name)

        # return nova.servers.create(
        #     server_name,
        #     "",
        #     flavor=flavor_id,
        #     nics=[{"net-id": net_id}],
        #     key_name=auth_key_name,
        #     block_device_mapping_v2=bdm,
        # )
