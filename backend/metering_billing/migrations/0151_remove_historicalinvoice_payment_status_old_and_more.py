# Generated by Django 4.0.5 on 2023-01-13 21:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0150_auto_20230113_2128"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalinvoice",
            name="payment_status_old",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="payment_status_old",
        ),
    ]
