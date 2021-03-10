import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_slack import slack_message
from sshpubkeys import SSHKey

from .validators import validate_public_key
from userdb.models import Region, Team, TeamMember


User = get_user_model()

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
        User,
        related_name="keypairs",
        related_query_name="keypair",
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Keypair name"), max_length=50, unique=True)
    public_key = models.TextField(_("SSH public key"), validators=[validate_public_key])
    fingerprint = models.CharField(max_length=47, editable=False)

    class Meta:
        unique_together = [["user", "public_key"]]

    def save(self, *args, **kwargs):
        # Set fingerprint
        ssh = SSHKey(self.public_key)
        ssh.parse()
        self.fingerprint = ssh.hash_md5()[4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def get_default_server_lease_expiry():
    return timezone.now() + datetime.timedelta(days=settings.SERVER_LEASE_DEFAULT_DAYS)


class ServerLease(models.Model):
    server_id = models.UUIDField(unique=True, editable=False)
    server_name = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_renewed_at = models.DateTimeField(auto_now=True, editable=False)
    expiry = models.DateTimeField(
        default=get_default_server_lease_expiry, blank=True, null=True
    )
    renewal_count = models.PositiveIntegerField(default=0, editable=False)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="server_leases", editable=False
    )
    assigned_teammember = models.ForeignKey(
        TeamMember, on_delete=models.PROTECT, related_name="server_leases",
    )
    shelved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    @property
    def has_expired(self):
        if self.expiry is None:
            return False
        return timezone.now() > self.expiry

    @property
    def renewal_url(self):
        return reverse(
            "openstack:server_lease_renewal",
            kwargs={"server_id": self.server_id, "renewal_count": self.renewal_count},
        )

    def renew_lease(self, days=settings.SERVER_LEASE_DEFAULT_DAYS, user=None):
        self.expiry = timezone.now() + datetime.timedelta(days=days)
        self.renewal_count += 1
        if user:
            self.user = user
        self.save()

    def send_email_renewal_reminder(self, request):
        """Send an email renewal reminder"""
        user = self.assigned_teammember.user
        expiry_days = (self.expiry - timezone.now()).days
        context = {
            "user": user,
            "server_name": self.server_name,
            "renewal_link": request.build_absolute_uri(self.renewal_url),
            "expiry_days": expiry_days,
        }
        subject = render_to_string(
            "openstack/email/server_lease_expiry_reminder_subject.txt", context
        )
        text_content = render_to_string(
            "openstack/email/server_lease_expiry_reminder_email.txt", context
        )
        html_content = render_to_string(
            "openstack/email/server_lease_expiry_reminder_email.html", context
        )
        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content,
            fail_silently=False,
        )

    def __str__(self):
        return (
            f"Lease for server '{self.server_name}', belonging to '{self.tenant.team.name}' "
            f"at {self.tenant.region.name}"
        )


class ActionLog(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
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
    max_volume_size_gb = models.IntegerField(
        _("Maximum allowed volume size in GB"), default=5000
    )

    def __str__(self):
        return str(self.region)


def get_tenant_for_team(team, region):  # TODO delete this once refactoring complete
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name=region))
    if not tenant:
        return None
    if len(tenant) > 1:
        return None
    return tenant[0]
