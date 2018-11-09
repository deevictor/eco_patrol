from django.db import models


class Feedback(models.Model):
    """Обратная связь."""
    name = models.CharField(
        max_length=254,
        verbose_name='Имя'
    )
    description = models.TextField(
        verbose_name='Текст сообщения'
    )
    pub_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания сообщения'
    )

    def __str__(self):
        name, pub_time = self.name, self.pub_time
        return f'{name} {pub_time}'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
