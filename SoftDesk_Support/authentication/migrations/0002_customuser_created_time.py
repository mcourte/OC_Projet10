# Generated by Django 5.0.6 on 2024-06-19 14:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date de création'),
        ),
    ]
