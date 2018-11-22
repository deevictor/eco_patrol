# coding: utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserForm(UserCreationForm):
    """Форма сгенерированная из модели `user.User`
    для регистрации новых юзеров

    Опции полей:
    classes (`form-control`): для стилей Bootstrap
    classes (`selectpicker`): для стилей Bootstrap
    placeholder: отображается в полях input
    option (`point`): поле скрыто

    :model:
    """

    agree = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agree'].label = "согласие на обработку данных"

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Пароль'}
        )

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}
        )

    class Meta:
        model = User
        fields = (
            'username', 'password1', 'password2', 'first_name', 'last_name',
            'middle_name', 'phone', 'email', 'city', 'agree'
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Логин',
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Фамилия',
                'class': 'form-control'
            }),
            'middle_name': forms.TextInput(attrs={
                'placeholder': 'Отчество',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Телефон',
                'class': 'form-control',
                'id': 'id_user_phone'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control',
                'id': 'id_user_email'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Город',
                'class': 'form-control'
            }),
        }


class LoginForm(AuthenticationForm):
    """Форма сгенерированная из модели `user.User` для входа  юзеров."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Логин',
                'id': 'id_login'
            }
        )

        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Пароль'}
        )
