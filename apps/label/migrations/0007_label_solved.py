# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-21 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0006_label_in_top'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='solved',
            field=models.BooleanField(default=False, verbose_name='Проблема решена'),
        ),
    ]