# Generated by Django 4.0.5 on 2022-12-07 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metering_billing', '0103_alter_historicalplanversion_usage_billing_frequency_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalinvoice',
            name='invoice_id',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_id',
        ),
        migrations.AddField(
            model_name='historicalinvoice',
            name='due_date',
            field=models.DateTimeField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalinvoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AddField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
