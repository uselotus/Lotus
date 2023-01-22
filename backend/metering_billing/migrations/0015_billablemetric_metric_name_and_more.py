# Generated by Django 4.0.5 on 2022-09-21 05:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "metering_billing",
            "0014_rename_recurring_billablemetric_carries_over_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="billablemetric",
            name="metric_name",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name="billablemetric",
            unique_together={("organization", "metric_name")},
        ),
    ]
