# Generated by Django 4.0.5 on 2022-12-05 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0101_historicalsubscriptionrecord_fully_billed_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoicelineitem",
            name="associated_subscription_record",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="line_items",
                to="metering_billing.subscriptionrecord",
            ),
        ),
    ]
