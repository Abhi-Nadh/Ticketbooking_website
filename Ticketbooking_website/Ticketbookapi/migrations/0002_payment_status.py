# Generated by Django 4.1.2 on 2023-06-15 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ticketbookapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=200)),
                ('payment_id', models.CharField(default=None, max_length=200, null=True)),
                ('payment_signature', models.CharField(default=None, max_length=200, null=True)),
                ('reciept_num', models.CharField(max_length=200, null=True)),
                ('payment_complete', models.IntegerField(default=0)),
                ('paydone', models.DateTimeField(auto_now_add=True)),
                ('customer_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticketbookapi.booking_models')),
            ],
        ),
    ]