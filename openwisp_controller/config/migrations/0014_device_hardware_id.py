# Generated by Django 2.0.9 on 2018-10-25 14:06

from django.db import migrations, models

from openwisp_controller.config import settings as app_settings


class Migration(migrations.Migration):
    dependencies = [("config", "0013_last_ip_management_ip_and_status_applied")]

    operations = [
        migrations.AddField(
            model_name="device",
            name="hardware_id",
            field=models.CharField(**(app_settings.HARDWARE_ID_OPTIONS)),
        )
    ]
