# Generated by Django 5.2.4 on 2025-07-18 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_reservation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reservation',
        ),
    ]
