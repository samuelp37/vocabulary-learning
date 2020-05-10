# Generated by Django 2.2.2 on 2020-03-22 19:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Last name')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Short Gender')),
                ('gender', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Gender')),
            ],
            options={
                'verbose_name': 'Gender',
                'verbose_name_plural': 'Genders',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Newspaper',
                'verbose_name_plural': 'Newspapers',
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Title')),
                ('language', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Language')),
            ],
            options={
                'verbose_name': 'Support',
                'verbose_name_plural': 'Supports',
            },
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_word', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Original word')),
                ('translation', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Translation')),
                ('context_sentence', models.TextField(blank=True, default='', null=True, verbose_name='Context original sentence')),
                ('translation_context_sentence', models.TextField(blank=True, default='', null=True, verbose_name='Translation of the context sentence')),
                ('date_added', models.DateField(default=datetime.date.today, verbose_name='Date of edition')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Word')),
                ('gender', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Gender')),
                ('language', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Language')),
            ],
            options={
                'verbose_name': 'Word',
                'verbose_name_plural': 'Words',
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(default=datetime.date.today, verbose_name='Date of edition')),
                ('context_sentence', models.TextField(blank=True, default='', null=True, verbose_name='Context original sentence')),
                ('translation_context_sentence', models.TextField(blank=True, default='', null=True, verbose_name='Translation of the context sentence')),
                ('original_word', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='original_word', to='dictionary.Word', verbose_name='Original word')),
                ('translated_word', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='translated_word', to='dictionary.Word', verbose_name='Translated word')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('support_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dictionary.Support')),
                ('subtitle', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Subtitle')),
                ('nb_pages', models.IntegerField(blank=True, default=-1, null=True, verbose_name='Number of pages')),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Author')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=('dictionary.support',),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('support_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dictionary.Support')),
                ('link', models.TextField(blank=True, default='', null=True, verbose_name='Link to the article')),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Author')),
                ('newspaper', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dictionary.Newspaper')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
            bases=('dictionary.support',),
        ),
    ]
