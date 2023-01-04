# Generated by Django 4.0.5 on 2023-01-04 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metering_billing', '0137_historicalmetric_mat_views_provisioned_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
                ('tag_group', models.CharField(choices=[('plan', 'Plan')], max_length=15)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='metering_billing.organization')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='plans', to='metering_billing.tag'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('organization', 'tag_name', 'tag_group'), name='unique_with_tag_group'),
        ),
    ]
