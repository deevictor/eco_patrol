# coding: utf-8
from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """Форма модели `feedback.Feedback` для отправки сообщений
    пользователями
    Всем полям добавлен класс `form-control` для стилей Bootstrap
    """

    class Meta:
        model = Feedback
        fields = ('name', 'description',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'email': {
                'required': 'Для обратной связи укажите ваш email'
            },
            'description': {
                'required': 'Вы забыли написать текст сообщения'
            }
        }
