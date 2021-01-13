# Generated by Django 3.1.1 on 2021-01-13 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import openstack.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("openstack", "0017_auto_20210104_1500"),
    ]

    operations = [
        migrations.CreateModel(
            name="KeyPair",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Keypair name"
                    ),
                ),
                (
                    "public_key",
                    models.TextField(
                        unique=True,
                        validators=[openstack.validators.validate_public_key],
                        verbose_name="SSH public key",
                    ),
                ),
                ("fingerprint", models.CharField(editable=False, max_length=47)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keypairs",
                        related_query_name="keypair",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
