# Generated by Django 4.1.2 on 2023-06-19 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticketbookapi', '0009_remove_payment_status_movie_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_models',
            name='language',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
