# Generated by Django 2.2.2 on 2020-04-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0016_auto_20200425_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjective',
            name='plural',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Plural'),
        ),
    ]
