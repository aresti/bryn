# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-30 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdb', '0019_auto_20160716_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='disable_new_instances',
            field=models.BooleanField(default=False),
        ),
    ]