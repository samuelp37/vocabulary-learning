# Generated by Django 2.2.2 on 2020-04-25 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0014_auto_20200425_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expression',
            name='word',
        ),
        migrations.AddField(
            model_name='expression',
            name='expression',
            field=models.TextField(default='', verbose_name='Expression'),
        ),
    ]
