# coding: utf-8
import os

from django.conf import settings


class AdminYMapMixin:
    """Подключаем скрипт Яндекс карт
    и свой js-файл из папки static/grappelli/map.js
    """

    class Media:
        js = [
            'https://api-maps.yandex.ru/2.1/?lang=ru_RU',
            os.path.join(settings.STATIC_URL, 'grappelli/map.js'),
        ]
        css = {
            'all': [
                os.path.join(settings.STATIC_URL, 'grappelli/map.css'),
            ]
        }
