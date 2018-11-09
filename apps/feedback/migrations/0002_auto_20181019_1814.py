# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='email',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(max_length=254, verbose_name='Имя'),
        ),
    ]