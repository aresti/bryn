import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_slack import slack_message
from sshpubkeys import SSHKey

from .validators import validate_public_key
from userdb.models import Team, Region


# Region model would ideally be in this app, but to avoid legacy migration issues it remains in userdb


class Tenant(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tenants")
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    created_tenant_id = models.CharField(max_length=50)
    auth_password = models.CharField(max_length=50, blank=True)
    created_network_id = models.CharField(max_length=50, blank=True)

    # TODO property decorator
    def get_tenant_name(self):
        return "bryn:%d_%s" % (self.team.pk, self.team.name)

    # TODO property decorator
    def get_tenant_description(self):
        return "%s (%s)" % (self.team.name, self.team.creator.last_name)

    def get_network_id(self):
        if self.region.regionsettings.requires_network_setup:
            return self.created_network_id
        else:
            # i.e. warwick
            return self.region.regionsettings.public_network_id

    def __str__(self):
        return self.get_tenant_name()


class KeyPair(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="keypairs",
        related_query_name="keypair",
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Keypair name"), max_length=50, unique=True)
    public_key = models.TextField(
        _("SSH public key"), unique=True, validators=[validate_public_key]
    )
    fingerprint = models.CharField(max_length=47, editable=False)

    def save(self, *args, **kwargs):
        # Set fingerprint
        ssh = SSHKey(self.public_key)
        ssh.parse()
        self.fingerprint = ssh.hash_md5()[4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ActionLog(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=None, null=True, on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    error = models.BooleanField()

    def save(self, *args, **kwargs):
        super(ActionLog, self).save(self, *args, **kwargs)
        if self.error:
            slack_message("openstack/error.slack", {"log": self})
        else:
            slack_message("openstack/success.slack", {"log": self})

    def __str__(self):
        if self.error:
            error_type = "ERROR"
        else:
            error_type = "SUCCESS"
        return "%s %s %s %s" % (self.date, error_type, self.tenant, self.message)


class HypervisorStats(models.Model):
    region = models.OneToOneField(Region, on_delete=models.CASCADE)

    last_updated = models.DateTimeField(auto_now=True)

    hypervisor_count = models.IntegerField()
    disk_available_least = models.IntegerField()
    free_disk_gb = models.IntegerField()
    free_ram_mb = models.IntegerField()
    local_gb = models.IntegerField()
    local_gb_used = models.IntegerField()
    memory_mb = models.IntegerField()
    memory_mb_used = models.IntegerField()
    running_vms = models.IntegerField()
    vcpus = models.IntegerField()
    vcpus_used = models.IntegerField()


class RegionSettings(models.Model):
    region = models.OneToOneField(Region, on_delete=models.CASCADE)
    public_network_name = models.CharField(max_length=50)
    public_network_id = models.CharField(max_length=50)
    requires_network_setup = models.BooleanField(default=False)
    floating_ip_pool = models.CharField(max_length=50, blank=True)
    horizon_endpoint = models.URLField(blank=True)  # TODO: remove blank after migration

    def __str__(self):
        return str(self.region)


def get_tenant_for_team(team, region):  # TODO delete this once refactoring complete
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name=region))
    if not tenant:
        return None
    if len(tenant) > 1:
        return None
    return tenant[0]
