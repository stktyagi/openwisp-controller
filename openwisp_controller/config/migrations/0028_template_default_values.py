# Generated by Django 3.0.3 on 2020-06-29 23:54

import collections

import jsonfield.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("config", "0027_add_indexes_on_ip_fields")]

    operations = [
        migrations.AddField(
            model_name="template",
            name="default_values",
            field=jsonfield.fields.JSONField(
                blank=True,
                default=dict,
                dump_kwargs={"ensure_ascii": False, "indent": 4},
                help_text=(
                    "A dictionary containing the default values for "
                    "the variables used by this template; these default "
                    "variables will be used during schema validation."
                ),
                load_kwargs={"object_pairs_hook": collections.OrderedDict},
                verbose_name="Default Values",
            ),
        )
    ]
