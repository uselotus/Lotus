# Generated by Django 4.0.5 on 2022-08-28 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("metering_billing", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="users",
        ),
        migrations.RemoveField(
            model_name="user",
            name="company_name",
        ),
        migrations.AddField(
            model_name="user",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="metering_billing.organization",
            ),
        ),
    ]
