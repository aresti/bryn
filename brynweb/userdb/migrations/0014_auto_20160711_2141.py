# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 21:41
from __future__ import unicode_literals

from django.db import migrations

def add_regions(apps, schema_editor):
    Region = apps.get_model("userdb", "Region")
    Region(name='warwick', description="University of Warwick").save()
    Region(name='bham', description="University of Birmingham").save()
    Region(name='cardiff', description="University of Cardiff").save()

class Migration(migrations.Migration):

    dependencies = [
        ('userdb', '0013_auto_20160711_2132'),
    ]

    operations = [
        migrations.RunPython(add_regions),
    ]
