# coding: utf-8
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Comment, Label


class LabelForm(forms.ModelForm):
    """Форма сгенерированная из модели `label.Label`
    для создания меток на карте пользователями

    Опции полей:
    classes (`form-control`): для стилей Bootstrap
    classes (`selectpicker`): для стилей Bootstrap
    placeholder: отображается в полях input
    option (`point`): поле скрыто

    :model:
    """

    def __init__(self, *args, **kwargs):
        super(LabelForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория метки'
        self.fields['attach'].label = "Выберите файлы"

    class Meta:
        model = Label
        fields = (
            'about', 'category', 'name', 'phone',
            'email', 'description', 'attach', 'point'
        )
        widgets = {
            'about': forms.TextInput(attrs={
                'placeholder': 'Местоположение',
                'class': 'form-control font-color-white'
            }),
            'category': forms.Select(attrs={
                'id': 'categorySelect',
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Телефон',
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Описание',
                'class': 'form-control'
            }),
            'point': forms.HiddenInput(),
            'attach': forms.ClearableFileInput(attrs={
                'id': 'file',
                'multiple': 'multiple'
            }),
        }

    def clean_attach(self):
        attach = self.cleaned_data['attach']
        if attach and attach.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(
                'Среди прикрепленных файлов есть файлы с недопустимым размером'
            )
        return attach


class CommentForm(forms.ModelForm):
    """Форма для отправки комментариев к метке"""

    class Meta:
        model = Comment
        fields = ('name', 'text', 'label')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Ваш комментарий',
                'class': 'form-control selectpicker'
            }),
            'label': forms.HiddenInput(),
        }
