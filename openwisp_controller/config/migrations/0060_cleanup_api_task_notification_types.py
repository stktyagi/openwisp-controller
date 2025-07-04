# Generated by Django 5.2.2 on 2025-06-30 11:34

from django.db import migrations


def cleanup_api_task_notification_types(apps, schema_editor):
    if not apps.is_installed("openwisp_notifications"):
        return
    Notification = apps.get_model("openwisp_notifications", "Notification")
    NotificationSetting = apps.get_model(
        "openwisp_notifications", "NotificationSetting"
    )
    NotificationSetting.objects.filter(
        type__in=["api_task_error", "api_task_recovery"]
    ).delete()
    Notification.objects.filter(
        type__in=["api_task_error", "api_task_recovery"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0059_zerotier_templates_ow_zt_to_global"),
    ]

    operations = [
        migrations.RunPython(
            cleanup_api_task_notification_types, reverse_code=migrations.RunPython.noop
        ),
    ]
