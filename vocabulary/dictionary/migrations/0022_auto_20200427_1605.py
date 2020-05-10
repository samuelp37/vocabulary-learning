# Generated by Django 2.2.2 on 2020-04-27 14:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionary', '0021_auto_20200426_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_quizz', models.DateField(default=datetime.date.today, verbose_name='Date of the quizz')),
            ],
            options={
                'verbose_name': 'Quizz',
                'verbose_name_plural': 'Quizz',
            },
        ),
        migrations.CreateModel(
            name='QuizzItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_to_translate', models.BooleanField(default=False)),
                ('delivered_on', models.DateTimeField(default=datetime.datetime(2020, 4, 27, 16, 5, 29, 397967), verbose_name='Date of delivery')),
                ('delta_reply', models.FloatField(default=-1, verbose_name='Duration reply (s)')),
                ('success', models.BooleanField(default=False)),
                ('translation', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Translation')),
            ],
            options={
                'verbose_name': 'Quizz item',
                'verbose_name_plural': 'Quizz items',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='translations',
            field=models.ManyToManyField(through='dictionary.TranslationLinkArticle', to='dictionary.Translation'),
        ),
        migrations.AlterField(
            model_name='book',
            name='translations',
            field=models.ManyToManyField(through='dictionary.TranslationLink', to='dictionary.Translation'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='translations',
            field=models.ManyToManyField(through='dictionary.TranslationLinkDiscussion', to='dictionary.Translation'),
        ),
        migrations.CreateModel(
            name='QuizzLinkItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizz', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Quizz')),
                ('quizz_item', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.QuizzItem')),
            ],
            options={
                'verbose_name': 'Quizz - Item',
                'verbose_name_plural': 'Quizz - Items',
            },
        ),
        migrations.AddField(
            model_name='quizz',
            name='items',
            field=models.ManyToManyField(through='dictionary.QuizzLinkItem', to='dictionary.QuizzItem'),
        ),
        migrations.AddField(
            model_name='quizz',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]