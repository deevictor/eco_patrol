# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-04 15:36
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import base.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254, unique=True, verbose_name='Заголовок')),
                ('color', base.fields.ColorField(blank=True, default='#FF0000', max_length=18, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Категория метки',
                'verbose_name_plural': 'Категории меток',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('submit_date', models.DateTimeField(auto_now=True, verbose_name='Дата/время отправки')),
                ('approved', models.BooleanField(default=False, verbose_name='Одобрено')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-submit_date',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='labels/')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(blank=True, max_length=300, null=True, verbose_name='Местоположение')),
                ('description', models.TextField(verbose_name='Описание')),
                ('name', models.CharField(max_length=254, validators=[django.core.validators.RegexValidator(message='Имя не может содержать цифры', regex='^[a-zA-Zа-яА-Я\\s]+$')], verbose_name='ФИО')),
                ('phone', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='Должно содержать только цифры, проблел и символы -.,()', regex='^[0-9-.,+\\s()]+$')], verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('point', models.CharField(max_length=64, unique=True, verbose_name='Точка на карте')),
                ('approved', models.BooleanField(default=True, verbose_name='Одобрено админом')),
                ('in_top', models.BooleanField(default=False, verbose_name='Вывести в топ')),
                ('solved', models.BooleanField(default=False, verbose_name='Проблема решена')),
                ('decision', models.FileField(blank=True, null=True, upload_to='decision/', verbose_name='Решение')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания метки')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='label.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Метка на карте',
                'verbose_name_plural': 'Метки на карте',
            },
        ),
        migrations.AddField(
            model_name='image',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.Label'),
        ),
        migrations.AddField(
            model_name='comment',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='label.Label', verbose_name='Метка на карте'),
        ),
    ]
