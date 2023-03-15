# Generated by Django 4.0.5 on 2023-03-02 20:18

from django.db import migrations


def transfer_to_brs(apps, schema_editor):
    SubscriptionRecord = apps.get_model("metering_billing", "SubscriptionRecord")
    BillingRecord = apps.get_model("metering_billing", "BillingRecord")
    InvoiceLineItem = apps.get_model("metering_billing", "InvoiceLineItem")
    for sr in SubscriptionRecord.objects.all():
        bp = sr.billing_plan
        components = bp.plan_components.all()
        recurring_charges = bp.recurring_charges.all()
        for component in components:
            br = BillingRecord.objects.create(
                organization=sr.organization,
                subscription=sr,
                component=component,
                start_date=sr.usage_start_date,
                end_date=sr.end_date,
                invoicing_dates=[sr.end_date],
                next_invoicing_date=sr.end_date,
                fully_billed=sr.fully_billed,
                unadjusted_duration_microseconds=sr.unadjusted_duration_microseconds,
            )
            for invoice_line_items in InvoiceLineItem.objects.filter(
                associated_subscription_record=sr, associated_plan_component=component
            ):
                invoice_line_items.associated_billing_record = br
                invoice_line_items.save()
        for charge in recurring_charges:
            BillingRecord.objects.create(
                organization=sr.organization,
                subscription=sr,
                recurring_charge=charge,
                start_date=sr.usage_start_date,
                end_date=sr.end_date,
                invoicing_dates=[sr.end_date],
                next_invoicing_date=sr.end_date,
                fully_billed=sr.fully_billed,
                unadjusted_duration_microseconds=sr.unadjusted_duration_microseconds,
            )
            for invoice_line_items in InvoiceLineItem.objects.filter(
                associated_subscription_record=sr, associated_recurring_charge=charge
            ):
                invoice_line_items.associated_billing_record = br
                invoice_line_items.save()


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0221_trigger_on_br"),
    ]

    operations = [
        migrations.RunPython(transfer_to_brs),
    ]
