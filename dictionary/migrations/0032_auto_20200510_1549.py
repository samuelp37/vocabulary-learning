# Generated by Django 3.0.6 on 2020-05-10 13:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0031_auto_20200510_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzitem',
            name='delivered_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 10, 15, 49, 7, 434754), null=True, verbose_name='Date of delivery'),
        ),
    ]
