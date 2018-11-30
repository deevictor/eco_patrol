# coding: utf-8
from django.http import JsonResponse
from django.template.loader import get_template

from .forms import CommentForm, LabelForm
from .models import Image, Label


def labels_json(request):
    """Возвращает гео-словарь меток на карте.
    Данные берутся из model: `label.Label`.
    Отображаются записи только те, что утверждены админом
    Словарь можно получить по ссылке
    """
    geos = []
    SOLVED_COLOR = '#0095b6'
    icon_type = 'darkgreenDotIcon'

    for label in Label.objects.filter(approved=True).select_related(
            'category'
    ).prefetch_related('image_set'):
        # Если метка решена делаем голубой и убираем точку внутри метки,
        # иначе если метка имеет категорию,
        # задаем цвет этой категории, иначе ее цвет #000
        color = '#000000'
        if label.solved:
            color = SOLVED_COLOR
            icon_type = 'icon'
        elif label.category:
            color = label.category.color

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
            'comments': comments,
            'decision': label.decision.url
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
                'hintContent': f'<strong>{label.category.title}</strong>',
                'decision': label.decision.url
            },
            'options': {
                'preset': f'islands#{icon_type}',
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


def label_form(request):
    """Метод для отправки формы без перезагрузки.
    Создание метки на карте пользователем.
    Используемая модель `label.Label`

    :return: словарь с результатом отправки:
        error (bool): наличие ошибки
        data (dict): данные формы
        message (str): описание ошибки
    """
    result = {'errors': False, 'data': {}, 'message': ''}

    if request.method == 'POST' and request.is_ajax():
        # Автоматически пробрасываем юзернейм для определения метки

        username = None

        if request.user:
            username = request.user.get_username()

        data = {'name': username}
        data.update(request.POST.dict())

        form = LabelForm(data, request.FILES)
        if form.is_valid():
            instance = form.save()
            for img in request.FILES.getlist('attach'):
                i = Image(
                    label=Label.objects.get(id=instance.id),
                    image=img
                )
                i.save()
            result['message'] = 'Сообщение отправлено!'
        else:
            result.update(
                errors=True,
                data=form.errors,
                message='Исправьте ошибки формы!'
            )

    return JsonResponse(result)


def ajax_comment(request):
    """Метод для отправки комментария без перезагрузки страницы
    """
    result = {'errors': False, 'data': {}, 'message': ''}
    if request.method == 'POST' and request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid() and form.save():
            result['message'] = 'Сообщение отправлено!'
        else:
            result.update(
                errors=True,
                data=form.errors,
                message='Исправьте ошибки формы!'
            )
    return JsonResponse(result)
