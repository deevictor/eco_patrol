# coding: utf-8
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import InspectorForm


@login_required
def inspector_request_async(request):
    """Метод для запроса статуса инспектора."""

    result = {'errors': False, 'data': {}, 'message': ''}
    template = 'user/inspector_form.html'
    form = InspectorForm(request.POST or None, instance=request.user)
    context = {"form": form}

    if request.method == 'POST' and request.is_ajax():
        if form.is_valid():
            form.save()
            result['status'] = True
            result['message'] = 'Данные отправлены!'
        else:
            result.update(
                status=False,
                errors=form.errors,
                message='Исправьте ошибки формы!'
            )

        return JsonResponse(result)

    return TemplateResponse(request, template, context)
