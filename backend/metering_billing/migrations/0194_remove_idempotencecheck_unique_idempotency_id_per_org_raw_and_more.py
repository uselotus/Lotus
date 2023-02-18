# Generated by Django 4.0.5 on 2023-02-18 22:12

import uuid

from django.conf import settings
from django.db import migrations, models


def fill_uuid(apps, schema_editor):
    IdempotenceCheck = apps.get_model("metering_billing", "IdempotenceCheck")
    for check in IdempotenceCheck.objects.all():
        check.uuidv5_idempotency_id = uuid.uuid5(
            settings.IDEMPOTENCY_ID_NAMESPACE, check.idempotency_id
        )
        check.save()


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0193_auto_20230218_2202"),
    ]

    operations = [
        migrations.AddField(
            model_name="idempotencecheck",
            name="uuidv5_idempotency_id",
            field=models.UUIDField(null=True),
        ),
    ]
