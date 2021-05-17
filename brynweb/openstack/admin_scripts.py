from openstack.service import OpenstackService
from openstack.models import Tenant


class ExistingTenantError(Exception):
    pass


def setup_openstack_project(team, region):
    """
    Setup an openstack project (tenant) for a team at a particular region.
    """
    # No duplicate team/region combinations
    if Tenant.objects.filter(team=team, region=region).count():
        raise ExistingTenantError(
            f"There is an existing project for '{team.name}' at '{region.name}'."
        )

    # Create (but don't save) a tenant
    tenant = Tenant(team=team, region=region)

    # Get an admin client and create the project
    admin_client = OpenstackService(region=region)
    domain = "default"
    project_name = tenant.get_tenant_name()

    openstack_project = admin_client.keystone.projects.create(
        project_name, domain, enabled=True
    )

    # Update & save Bryn tenant record
    tenant.created_tenant_id = openstack_project.id
    tenant.create_tenant_name = project_name
    tenant.save()

    # Set quotas
    admin_client.nova.quotas.update(
        openstack_project.id, cores=32, ram=270000, instances=8
    )
    admin_client.cinder.quotas.update(openstack_project.id, volumes=20, gigabytes=2200)

    # Grant _member_ role to Bryn 'service user'
    username = admin_client.auth_settings["SERVICE_USERNAME"]
    service_user = admin_client.keystone.users.list(name=username)[0]
    role = admin_client.keystone.roles.list(name="_member_")[0]
    admin_client.keystone.roles.grant(
        role, user=service_user, project=openstack_project
    )

    # Create default security rules
    project_client = OpenstackService(tenant=tenant)
    security_group_id = project_client.neutron.list_security_groups(name="default")[
        "security_groups"
    ][0]["id"]

    ingress_ports = [22, 80, 443]
    rule_defaults = {
        "security_group_id": security_group_id,
        "direction": "ingress",
        "protocol": "tcp",
        "remote_group_id": None,
        "remote_ip_prefix": "0.0.0.0/0",
    }

    for port in ingress_ports:
        rule = rule_defaults
        rule["port_range_min"] = port
        rule["port_range_max"] = port
        project_client.neutron.create_security_group_rule({"security_group_rule": rule})

    # Update team
    team.tenants_available = True
    team.save()
