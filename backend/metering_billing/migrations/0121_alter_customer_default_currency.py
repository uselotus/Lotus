# Generated by Django 4.0.5 on 2022-12-14 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metering_billing', '0120_merge_20221214_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='default_currency',
            field=models.ForeignKey(blank=True, help_text='The currency the customer will be invoiced in', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='metering_billing.pricingunit'),
        ),
    ]
