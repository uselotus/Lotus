# Generated by Django 4.0.5 on 2022-10-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("metering_billing", "0035_remove_organization_stripe_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoricalFilter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("property_name", models.CharField(max_length=100)),
                (
                    "operator",
                    models.CharField(
                        choices=[("isin", "Is in"), ("isnotin", "Is not in")],
                        max_length=10,
                    ),
                ),
                ("comparison_value", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="NumericFilter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("property_name", models.CharField(max_length=100)),
                (
                    "operator",
                    models.CharField(
                        choices=[
                            ("gte", "Greater than or equal to"),
                            ("gt", "Greater than"),
                            ("eq", "Equal to"),
                            ("lt", "Less than"),
                            ("lte", "Less than or equal to"),
                        ],
                        max_length=10,
                    ),
                ),
                ("comparison_value", models.FloatField()),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="billablemetric",
            name="unique_with_property_name_and_sap",
        ),
        migrations.RemoveConstraint(
            model_name="billablemetric",
            name="unique_without_property_name_with_sap",
        ),
        migrations.RemoveConstraint(
            model_name="billablemetric",
            name="unique_with_property_name_without_sap",
        ),
        migrations.RemoveConstraint(
            model_name="billablemetric",
            name="unique_without_property_name_without_sap",
        ),
        migrations.RenameField(
            model_name="billablemetric",
            old_name="event_type",
            new_name="metric_type",
        ),
        migrations.RemoveField(
            model_name="billablemetric",
            name="stateful_aggregation_period",
        ),
        migrations.AddField(
            model_name="billablemetric",
            name="properties",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="billablemetric",
            name="aggregation_type",
            field=models.CharField(
                choices=[
                    ("count", "Count"),
                    ("sum", "Sum"),
                    ("max", "Max"),
                    ("unique", "Unique"),
                    ("latest", "Latest"),
                    ("average", "Average"),
                    ("min", "Min"),
                ],
                default="count",
                max_length=10,
            ),
        ),
        migrations.AddConstraint(
            model_name="billablemetric",
            constraint=models.UniqueConstraint(
                fields=(
                    "organization",
                    "event_name",
                    "aggregation_type",
                    "property_name",
                    "metric_type",
                ),
                name="unique_with_property_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="billablemetric",
            constraint=models.UniqueConstraint(
                condition=models.Q(("property_name", None)),
                fields=(
                    "organization",
                    "event_name",
                    "aggregation_type",
                    "metric_type",
                ),
                name="unique_without_property_name",
            ),
        ),
        migrations.AddField(
            model_name="billablemetric",
            name="categorical_filters",
            field=models.ManyToManyField(
                blank=True, to="metering_billing.categoricalfilter"
            ),
        ),
        migrations.AddField(
            model_name="billablemetric",
            name="numeric_filters",
            field=models.ManyToManyField(
                blank=True, to="metering_billing.numericfilter"
            ),
        ),
    ]
