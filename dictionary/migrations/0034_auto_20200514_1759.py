# Generated by Django 3.0.6 on 2020-05-14 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0033_auto_20200510_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(default='', max_length=100, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='', max_length=100, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='gender',
            name='gender',
            field=models.CharField(default='', max_length=20, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='gender',
            name='short',
            field=models.CharField(default='', max_length=1, verbose_name='Short Gender'),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='quizzitem',
            name='delivered_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 14, 17, 59, 23, 188510), null=True, verbose_name='Date of delivery'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Name'),
        ),
    ]