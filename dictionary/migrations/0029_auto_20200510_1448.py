# Generated by Django 3.0.6 on 2020-05-10 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0028_auto_20200510_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzitem',
            name='delivered_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 10, 14, 48, 35, 892480), null=True, verbose_name='Date of delivery'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=400, null=True, verbose_name='Slug'),
        ),
    ]
