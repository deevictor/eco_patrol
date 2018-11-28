# coding: utf-8
from collections import OrderedDict

from django import forms
from django.utils.safestring import mark_safe
from mezzanine.accounts.forms import ProfileForm


class ProfileForm(ProfileForm):
    """
    Форма отнаследованная от формы профиля мезанина
    для регистрации новых юзеров
    """

    agree = forms.BooleanField(required=True)
    fields_order = ("first_name", "last_name", "middle_name", "phone", "city",
                    "email", "username", "password1", "password2", "agree")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = OrderedDict(
            (field_name, self.fields[field_name])
            for field_name in self.fields_order
        )
        self.fields['agree'].label = mark_safe(
            'Я согласен на '
            '<a href="/static/attachments/agreement.pdf" target="_blank" '
            'class="contact-emphasized">обработку персональных данных</a>')
