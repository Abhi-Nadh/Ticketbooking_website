# Generated by Django 4.1.2 on 2023-06-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_show_site', '0004_movie_details_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie_details',
            name='trailer',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
