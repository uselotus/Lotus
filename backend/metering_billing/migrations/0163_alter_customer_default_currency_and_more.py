# Generated by Django 4.1.5 on 2023-01-16 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0162_remove_pricetier_batch_rounding_type_old_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="default_currency",
            field=models.ForeignKey(
                blank=True,
                help_text="The currency the customer will be invoiced in",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="customers",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="customerbalanceadjustment",
            name="amount_paid_currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="paid_adjustments",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="customerbalanceadjustment",
            name="pricing_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="adjustments",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invoices",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="invoicelineitem",
            name="pricing_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="line_items",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="default_currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="organizations",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="plancomponent",
            name="pricing_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="components",
                to="metering_billing.pricingunit",
            ),
        ),
        migrations.AlterField(
            model_name="planversion",
            name="pricing_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="versions",
                to="metering_billing.pricingunit",
            ),
        ),
    ]
