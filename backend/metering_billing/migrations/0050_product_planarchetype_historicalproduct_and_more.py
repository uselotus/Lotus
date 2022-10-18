# Generated by Django 4.0.5 on 2022-10-18 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('metering_billing', '0049_alter_historicalorganization_company_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('product_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('deprecated', 'Deprecated')], max_length=40)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_products', to='metering_billing.organization')),
            ],
            options={
                'unique_together': {('organization', 'product_id')},
            },
        ),
        migrations.CreateModel(
            name='PlanArchetype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('plan_archetype_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('parent_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_archetypes', to='metering_billing.product')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('product_id', models.CharField(db_index=True, default=uuid.uuid4, max_length=100)),
                ('status', models.CharField(choices=[('active', 'Active'), ('deprecated', 'Deprecated')], max_length=40)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='metering_billing.organization')),
            ],
            options={
                'verbose_name': 'historical product',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='billingplan',
            name='archetype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_plans', to='metering_billing.planarchetype'),
        ),
        migrations.AddField(
            model_name='historicalbillingplan',
            name='archetype',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='metering_billing.planarchetype'),
        ),
    ]
