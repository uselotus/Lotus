# Generated by Django 4.0.5 on 2022-12-15 21:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0124_auto_20221215_0521"),
    ]

    operations = [
        migrations.DeleteModel(
            name="HistoricalSubscription",
        ),
    ]
