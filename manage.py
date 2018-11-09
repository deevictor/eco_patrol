#!/usr/bin/env python
import os
from os import sys, path

if __name__ == '__main__':

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomap.settings_local')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)