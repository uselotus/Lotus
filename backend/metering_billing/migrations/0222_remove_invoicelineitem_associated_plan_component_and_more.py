# Generated by Django 4.0.5 on 2023-03-01 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metering_billing', '0221_auto_20230301_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicelineitem',
            name='associated_plan_component',
        ),
        migrations.RemoveField(
            model_name='invoicelineitem',
            name='associated_recurring_charge',
        ),
        migrations.RemoveField(
            model_name='invoicelineitem',
            name='associated_subscription_record',
        ),
    ]
