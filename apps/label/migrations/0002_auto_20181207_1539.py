# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Одобрено админом'),
        ),
        migrations.AlterField(
            model_name='label',
            name='decision',
            field=models.ImageField(blank=True, null=True, upload_to='decision/', verbose_name='Решение'),
        ),
    ]
