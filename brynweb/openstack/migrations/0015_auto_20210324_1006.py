# Generated by Django 3.1.1 on 2021-03-24 10:06

from django.db import migrations, models


def forward_populate_legacy_created_tenant_name(apps, schema_editor):
    Tenant = apps.get_model("openstack", "Tenant")
    db_alias = schema_editor.connection.alias
    for tenant in Tenant.objects.using(db_alias).all():
        legacy_name = f"bryn:{tenant.team.pk}_{tenant.team.name}"
        tenant.created_tenant_name = legacy_name
        tenant.save()


class Migration(migrations.Migration):

    dependencies = [
        ("openstack", "0014_auto_20210323_1349"),
    ]

    operations = [
        migrations.RemoveField(model_name="tenant", name="auth_password",),
        migrations.AddField(
            model_name="tenant",
            name="created_tenant_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RunPython(forward_populate_legacy_created_tenant_name),
    ]
