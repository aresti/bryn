# Generated by Django 3.1.1 on 2021-05-07 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("openstack", "0020_auto_20210506_1651"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serverlease",
            name="last_renewed_at",
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]