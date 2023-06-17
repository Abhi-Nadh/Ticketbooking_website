# Generated by Django 4.1.2 on 2023-06-16 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ticketbookapi', '0005_remove_payment_status_customer_details_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_status',
            name='movie_id',
        ),
        migrations.AddField(
            model_name='payment_status',
            name='customer_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ticketbookapi.booking_models'),
        ),
    ]