# Generated by Django 4.0.5 on 2022-12-12 21:32

from django.db import migrations, models

import metering_billing.utils.utils


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0114_auto_20221212_1837"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="inserted_at",
            field=models.DateTimeField(default=metering_billing.utils.utils.now_utc),
        ),
    ]
