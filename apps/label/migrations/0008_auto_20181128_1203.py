# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-28 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0007_label_solved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='approved',
            field=models.BooleanField(default=True, verbose_name='Одобрено админом'),
        ),
    ]
