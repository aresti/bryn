# Generated by Django 3.1.1 on 2021-01-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userdb", "0025_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="department",
            field=models.CharField(max_length=50, verbose_name="Department"),
        ),
        migrations.AlterField(
            model_name="team",
            name="institution",
            field=models.CharField(max_length=100, verbose_name="Institution"),
        ),
        migrations.AlterField(
            model_name="team",
            name="name",
            field=models.CharField(
                help_text="e.g. Bacterial pathogenomics group",
                max_length=50,
                unique=True,
                verbose_name="Group or team name",
            ),
        ),
    ]