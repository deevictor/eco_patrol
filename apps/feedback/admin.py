# coding: utf-8
from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    """Отображает страницу в админке с сообщениями от пользователей.
    Используемая модель `feedback.Feedback`
    """

    list_display = ('name', 'pub_time',)
    readonly_fields = ('pub_time',)


admin.site.register(Feedback, FeedbackAdmin)
