# coding: utf-8
from django.core.validators import RegexValidator
from django.db import models
from mezzanine.conf import settings as mezzanine_conf

from base.fields import ColorField


class Category(models.Model):
    """Категория меток"""
    title = models.CharField(
        max_length=254,
        unique=True,
        verbose_name='Заголовок'
    )
    color = ColorField(
        blank=True,
        verbose_name='Цвет',
        default='#FF0000'
    )

    class Meta:
        verbose_name = 'Категория метки'
        verbose_name_plural = 'Категории меток'

    def __str__(self):
        return self.title


class Label(models.Model):
    """Метка на карте"""

    about = models.CharField(
        max_length=300,
        verbose_name='Местоположение',
        blank=True, null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True, null=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    attach = models.ImageField(
        null=True, blank=True,
        upload_to='attach/',
        verbose_name='Прикрепленный файл'
    )
    name = models.CharField(
        max_length=254,
        verbose_name='ФИО',
        validators=[RegexValidator(
            regex=r'^[a-zA-Zа-яА-Я\s]+$',
            message='Имя не может содержать цифры'
        )]
    )
    phone = models.CharField(
        max_length=64,
        verbose_name='Телефон',
        validators=[RegexValidator(
            regex=r'^[0-9-.,+\s()]+$',
            message='Должно содержать только цифры, проблел и символы -.,()'
        )]
    )
    email = models.EmailField(
        verbose_name='Электронная почта'
    )
    point = models.CharField(
        max_length=64,
        verbose_name='Точка на карте',
        unique=True
    )
    approved = models.BooleanField(
        default=True,
        verbose_name='Одобрено админом'
    )
    in_top = models.BooleanField(
        default=False,
        verbose_name='Вывести в топ'
    )
    solved = models.BooleanField(
        default=False,
        verbose_name='Проблема решена'
    )
    decision = models.FileField(
        null=True, blank=True,
        upload_to='decision/',
        verbose_name='Решение'
    )
    pub_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания метки'
    )

    def __str__(self):
        return self.name

    @property
    def get_images(self):
        return [i.image.url for i in self.image_set.all()]

    class Meta:
        verbose_name = 'Метка на карте'
        verbose_name_plural = 'Метки на карте'

    def get_absolute_url(self):
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current().domain
        return "http://%s/?id_balloon=%s" % (current_site, self.id)


class Image(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='labels/')


class Comment(models.Model):
    """Комментарий к метке"""
    name = models.CharField(
        verbose_name='Имя',
        max_length=64
    )
    text = models.TextField('Комментарий')
    submit_date = models.DateTimeField('Дата/время отправки', auto_now=True)
    label = models.ForeignKey(
        Label,
        verbose_name='Метка на карте',
        related_name='comments',
        on_delete=models.CASCADE
    )
    approved = models.BooleanField('Одобрено', default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-submit_date',)

    def __str__(self):
        name, date = self.name, self.submit_date
        text = self.text[:mezzanine_conf.COMMENT_PREVIEW_SIZE] + '...'
        return f'[{name} {date}] {text}'
