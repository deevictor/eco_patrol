from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя."""

    phone = models.CharField(
        max_length=64,
        verbose_name='Телефон',
        validators=[RegexValidator(
            regex=r'^[0-9-.,+\s()]+$',
            message='Должно содержать только цифры, проблел и символы -.,()'
        )]
    )

    city = models.CharField(
        verbose_name='Город',
        max_length=64
    )

    is_inspector = models.BooleanField(
        'Статус инспектора',
        default=False,
    )

    middle_name = models.CharField(
        verbose_name='Отчество',
        validators=[RegexValidator(
            regex=r'^[a-zA-Zа-яА-Я\s]+$',
            message='Отчество не может содержать цифры'
        )],
        max_length=64,
        blank=True,
        null=True
    )

    registration = models.CharField(
        verbose_name='Прописка',
        max_length=128,
        blank=True,
        null=True
    )

    education = models.CharField(
        verbose_name='Образование',
        max_length=64,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
