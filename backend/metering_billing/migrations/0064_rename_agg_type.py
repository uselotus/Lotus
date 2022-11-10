# Generated by Django 4.0.5 on 2022-11-10 04:47

from django.db import migrations, models
from django.db.models import F, Q


def migrate_metric_type(apps, schema_editor):
    BillableMetric = apps.get_model("metering_billing", "BillableMetric")
    BillableMetric.objects.filter(metric_type="aggregation").update(
        metric_type="counter"
    )


def migrate_all_mins_to_max(apps, schema_editor):
    BillableMetric = apps.get_model("metering_billing", "BillableMetric")
    BillableMetric.objects.filter(usage_aggregation_type="min").update(usage_aggregation_type="max")


def migrate_stateful_other_to_max(apps, schema_editor):
    BillableMetric = apps.get_model("metering_billing", "BillableMetric")
    BillableMetric.objects.filter(
        ~Q(usage_aggregation_type="max") & ~Q(usage_aggregation_type="latest"),
        metric_type="stateful",
    ).update(usage_aggregation_type="max")


class Migration(migrations.Migration):

    dependencies = [
        ("metering_billing", "0063_alter_plancomponent_free_metric_units"),
    ]

    operations = [
        migrations.RenameField(
            model_name="billablemetric",
            old_name="aggregation_type",
            new_name="usage_aggregation_type",
        ),
        migrations.RenameField(
            model_name="historicalbillablemetric",
            old_name="aggregation_type",
            new_name="usage_aggregation_type",
        ),
        migrations.RunPython(migrate_all_mins_to_max),
        migrations.RunPython(migrate_metric_type),
        migrations.RunPython(migrate_stateful_other_to_max),
    ]
