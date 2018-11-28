from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    """Расширенная модель пользователя."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
