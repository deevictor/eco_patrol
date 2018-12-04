from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
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

    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Город'
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

    @property
    def get_admin_profile_url(self):
        """Возвращает ссылку на профиль пользователя в админке."""
        return reverse('admin:user_user_change', args=(self.pk,))


class City(models.Model):
    """Города для пользователей."""

    name = models.CharField(
        verbose_name='Город',
        max_length=64
    )

    latitude = models.DecimalField(
        verbose_name='Широта',
        max_digits=10,
        decimal_places=7
    )

    longitude = models.DecimalField(
        verbose_name='Долгота',
        max_digits=10,
        decimal_places=7
    )

    type_of_region = models.CharField(
        verbose_name='Тип региона',
        max_length=64
    )

    region = models.CharField(
        verbose_name='Регион',
        max_length=64
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.name},  {self.region} {self.type_of_region}'
