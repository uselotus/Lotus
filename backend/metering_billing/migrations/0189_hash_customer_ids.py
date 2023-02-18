# Generated by Django 4.0.5 on 2023-02-18 19:03

import uuid

from django.conf import settings
from django.db import migrations


def set_uuidv5_customer_id(apps, schema_editor):
    Customer = apps.get_model("metering_billing", "Customer")
    HistoricalCustomer = apps.get_model("metering_billing", "HistoricalCustomer")
    CUSTOMER_ID_NAMESPACE = settings.CUSTOMER_ID_NAMESPACE

    for customer in Customer.objects.all():
        customer.uuidv5_customer_id = uuid.uuid5(
            CUSTOMER_ID_NAMESPACE, customer.customer_id
        )
        customer.save()
    for historical_customer in HistoricalCustomer.objects.all():
        historical_customer.uuidv5_customer_id = uuid.uuid5(
            CUSTOMER_ID_NAMESPACE, historical_customer.customer_id
        )
        historical_customer.save()


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0188_customer_uuidv5_customer_id_and_more"),
    ]

    operations = [
        migrations.RunPython(
            set_uuidv5_customer_id, reverse_code=migrations.RunPython.noop
        ),
    ]
