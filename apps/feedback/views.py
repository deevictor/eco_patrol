# coding: utf-8
from django.shortcuts import render

from .forms import FeedbackForm


def contact(request):
    """Отображает страницу контактов

    Контексты:
    form (object): форма для отправки сообщений пользователями
    flag (bool):  если True то форма на странице не показывается
    """
    ctx = {}
    form = FeedbackForm()
    flag = False

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            flag = True

    ctx.update({
        'form': form,
        'flag': flag
    })

    return render(request, 'feedback/contact.html', ctx)
