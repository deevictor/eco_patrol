# coding: utf-8
from django import forms
from django.utils.safestring import mark_safe
from mezzanine.accounts.forms import ProfileForm

from .models import User


class UserRegisterForm(ProfileForm):
    """Форма регистрации новых пользователей."""

    agree = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agree'].label = mark_safe(
            'Я согласен на '
            '<a href="/static/attachments/agreement.pdf" target="_blank" '
            'class="contact-emphasized">обработку персональных данных</a>'
        )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "middle_name", "phone", "city",
                  "email", "username", "password1", "password2", "agree")


class InspectorForm(forms.ModelForm):
    """Форма для запроса статуса инспектора"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['middle_name'].widget.attrs['readonly'] = True
        self.fields['phone'].widget.attrs['readonly'] = True
        self.fields['registration'].required = True
        self.fields['education'].required = True

    class Meta:
        model = User
        fields = ("first_name", "last_name", "middle_name", "phone",
                  "registration", "education")
