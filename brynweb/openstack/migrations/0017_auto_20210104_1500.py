# Generated by Django 3.1.1 on 2021-01-04 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("openstack", "0016_auto_20201021_1111"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tenant",
            name="auth_password",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]