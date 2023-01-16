# Generated by Django 4.1.5 on 2023-01-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0162_remove_pricetier_batch_rounding_type_old_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalorganizationsetting",
            name="setting_group",
            field=models.CharField(
                blank=True,
                choices=[("stripe", "Stripe"), ("billing", "Billing")],
                max_length=64,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalorganizationsetting",
            name="setting_name",
            field=models.CharField(
                choices=[
                    (
                        "generate_customer_after_creating_in_lotus",
                        "Generate in Stripe after Lotus",
                    ),
                    ("subscription_filter_keys", "Subscription Filter Keys"),
                    ("payment_grace_period", "Payment Grace Period"),
                ],
                max_length=64,
            ),
        ),
        migrations.AlterField(
            model_name="organizationsetting",
            name="setting_group",
            field=models.CharField(
                blank=True,
                choices=[("stripe", "Stripe"), ("billing", "Billing")],
                max_length=64,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="organizationsetting",
            name="setting_name",
            field=models.CharField(
                choices=[
                    (
                        "generate_customer_after_creating_in_lotus",
                        "Generate in Stripe after Lotus",
                    ),
                    ("subscription_filter_keys", "Subscription Filter Keys"),
                    ("payment_grace_period", "Payment Grace Period"),
                ],
                max_length=64,
            ),
        ),
    ]
