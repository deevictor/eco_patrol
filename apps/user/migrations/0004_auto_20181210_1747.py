# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-10 17:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0003_auto_20181207_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name',), 'verbose_name': 'Город',
                     'verbose_name_plural': 'Города'},
        ),
    ]