# coding: utf-8
from django.http import JsonResponse
from django.template.loader import get_template

from base.constants import URL_SHARE

from .forms import LabelForm, CommentForm
from .models import Image, Label


def labels_json(request):
    """Возвращает гео-словарь меток на карте.
    Данные берутся из model: `label.Label`.
    Отображаются записи только те, что утверждены админом
    Словарь можно получить по ссылке
    """
    geos = []
    SOLVED_COLOR = '#3b5998'

    for label in Label.objects.filter(approved=True).select_related(
            'category'
    ).prefetch_related('image_set'):
        # Если метка решена делаем синей,
        # иначе если метка имеет категорию,
        # задаем цвет этой категории, иначе ее цвет #000
        if label.solved:
            color = SOLVED_COLOR
        elif label.category:
            color = label.category.color
        else:
            color = '#000000'
        comments = label.comments.filter(approved=True)
        template_message = get_template('label/balloon.html')
        balloon_content = template_message.render({
            'category': label.category.title,
            'images': label.get_images,
            'url': label.get_absolute_url(),
            'description': label.description,
            'name': label.name,
            'about': label.about,
            'form_comment': CommentForm(initial={'label': label.id}),
            'comments': comments
        })

        poly = {
            'type': 'Feature',
            'id': label.id,
            'geometry': {
                'type': 'Point',
                'coordinates': [float(i) for i in label.point.split(',')],
            },
            'properties': {
                'clusterCaption': label.category.title,
                'balloonContentBody': balloon_content,
                'category': label.category.title,
                'images': label.get_images,
                'url': label.get_absolute_url(),
                'description': label.description,
                'name': label.name,
                # текст при наведении мыши
                'hintContent': '<strong></strong>',
            },
            'options': {
                'preset': 'islands#darkgreenDotIcon',
                'iconColor': color,
                'iconCaptionMaxWidth': '50',
                'hideIconOnBalloonOpen': False,
            }
        }
        geos.append(poly)

    return JsonResponse({
        'type': 'FeatureCollection',
        'features': geos,
    })


def ajax_form(request):
    """Метод для отправки формы без перезагрузки.
    Создание метки на карте пользователем.
    Используемая модель `label.Label`

    :return: словарь с результатом отправки:
        error (bool): наличие ошибки
        data (dict): данные формы
        dn (str): описание ошибки
    """
    result = {'errors': False, 'data': {}, 'dn': ''}

    if request.method == 'POST' and request.is_ajax():
        form = LabelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print(instance.id)
            for img in request.FILES.getlist('attach'):
                i = Image(
                    label=Label.objects.get(id=instance.id),
                    image=img
                )
                i.save()
            result['dn'] = 'Сообщение отправлено!'
        else:
            response = {}
            for k in form.errors:
                response[k] = form.errors[k][0]
            result['errors'] = True
            result['data'] = response
            result['dn'] = 'Исправьте ошибки формы!'

    return JsonResponse(result)


def ajax_comment(request):
    """Метод для отправки комментария без перезагрузки страницы
    """
    result = {'errors': False, 'data': {}, 'dn': ''}
    if request.method == 'POST' and request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid() and form.save():
            result['dn'] = 'Сообщение отправлено!'
        else:
            result['errors'] = True
            result['data'] = {k: form.errors[k][0] for k in form.errors}
            result['dn'] = 'Исп равьте ошибки формы!'
    return JsonResponse(result)
