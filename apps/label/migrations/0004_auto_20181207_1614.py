# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0003_auto_20181207_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='decision',
            options={'verbose_name': 'Решение', 'verbose_name_plural': 'Решение'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Картинки', 'verbose_name_plural': 'Картинки'},
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='labels/', verbose_name='Картинка'),
        ),
    ]
