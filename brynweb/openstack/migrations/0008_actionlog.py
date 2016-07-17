# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 07:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openstack', '0007_tenant_created_network_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('error', models.BooleanField()),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openstack.Tenant')),
            ],
        ),
    ]