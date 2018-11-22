# coding: utf-8
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse


from .forms import LoginForm, UserForm


@csrf_exempt
def register(request):
    """Метод для отправки формы без перезагрузки.
    Регистрация пользователя.
    Используемая модель `user.User`

    :return: словарь с результатом отправки:
        error (bool): наличие ошибки
        data (dict): данные формы
        dn (str): описание ошибки
    """
    result = {'errors': False, 'data': {}, 'message': ''}

    if request.method == 'POST' and request.is_ajax():
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(
                request, username=username, password=raw_password
            )
            login(request, user)
            result['url'] = settings.LOGIN_REDIRECT_URL
            result['message'] = 'Вы зарегистрированы!'
        else:
            result.update(
                errors=True,
                data=form.errors,
                message='Исправьте ошибки формы!'
            )

    return JsonResponse(result)


@csrf_exempt
def login_user(request):
    """Метод для входа юзера без перезагрузки.
    Используемая модель `user.User`

    :return: словарь с результатом отправки:
        error (bool): наличие ошибки
        data (dict): данные формы
        dn (str): описание ошибки
    """
    result = {'errors': False, 'data': {}, 'message': ''}

    if request.method == 'POST' and request.is_ajax():
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(
                request, username=username, password=raw_password
            )
            if user is not None:
                login(request, user)
                result['url'] = settings.LOGIN_REDIRECT_URL
            else:
                result['message'] = 'Учетная запись не активирована!'
        else:
            reverse_html_link = '<br><a href="'\
                               + reverse('user:password_reset')\
                               + '">Сбросить пароль.</a>'
            form.non_field_errors()[0] += reverse_html_link
            result.update(
                errors=True,
                data=form.errors,
                message=form.non_field_errors()
            )

    return JsonResponse(result)
