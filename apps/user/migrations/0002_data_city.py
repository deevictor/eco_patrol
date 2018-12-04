# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    """Загружаем данные городов."""
    call_command('loaddata', 'cities.json')


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            load_fixture,
            reverse_code=migrations.RunPython.noop
        )
    ]
