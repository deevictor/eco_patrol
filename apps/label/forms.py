# coding: utf-8
from django import forms

from label.utils import LabelErrorsDict

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

    images = forms.FileField(label='Изображения', required=False,
                             widget=forms.ClearableFileInput(
                                 attrs={
                                     'class': 'form-control',
                                     'multiple': True, 'id': 'file'}))

    def __init__(self, *args, **kwargs):
        super(LabelForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория метки'

    class Meta:
        model = Label
        fields = (
            'about', 'category', 'name', 'phone',
            'email', 'description', 'point'
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
        }

    def full_clean(self):
        super().full_clean()
        self._errors = LabelErrorsDict(self._errors)


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
