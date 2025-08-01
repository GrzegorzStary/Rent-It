# Generated by Django 5.2.3 on 2025-07-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='house_number',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(default='Unknown', max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='street_name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
