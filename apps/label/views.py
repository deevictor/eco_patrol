# coding: utf-8
from django.http import JsonResponse
from django.template.loader import get_template

from user.models import User
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
    INSPECTOR_COLOR = 'darkGreen'
    icon_type = 'darkgreenDotIcon'
    has_balloon = False

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
            'decision': label.get_decisions
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
                'decision': label.get_decisions
            },
            'options': {
                'preset': f'islands#{icon_type}',
                'iconColor': color,
                'iconCaptionMaxWidth': '50',
                'hideIconOnBalloonOpen': False,
            }
        }
        geos.append(poly)

    for user in User.objects.filter(
            is_inspector=True, city__isnull=False
    ).select_related(
        'city'
    ):
        icon_type = 'darkGreenCircleIcon'
        color = INSPECTOR_COLOR
        template_message = get_template('label/inspector_balloon_form.html')
        if request.user.is_superuser:
            balloon_content = template_message.render({
                'user': user,
                'user_full_name':
                    f'{user.first_name} {user.middle_name} {user.last_name}'
            })
            cluster_caption = user.username
            open_balloon_on_click = True
            has_balloon = True
        else:
            balloon_content = None
            cluster_caption = None
            open_balloon_on_click = False

        inspector = {
            'type': 'Feature',
            'id': f'user_{user.id}',
            'geometry': {
                'type': 'Point',
                'coordinates': [user.city.latitude, user.city.longitude],
            },
            'properties': {
                'clusterCaption': cluster_caption,
                'balloonContentBody': balloon_content,
                'name': user.username,
                # текст при наведении мыши
                'hintContent': 'Инспекторы',
                # 1 для отображения в случае когда в городе всего один инспектор
                'iconContent': '1',
            },
            'options': {
                'preset': f'islands#{icon_type}',
                'iconColor': color,
                'iconCaptionMaxWidth': '50',
                'hideIconOnBalloonOpen': False,
                'openBalloonOnClick': open_balloon_on_click
            }
        }
        geos.append(inspector)

    return JsonResponse({
        'type': 'FeatureCollection',
        'features': geos,
        'clusterBalloon': has_balloon,
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
    success_message = 'Сообщение отправлено!'
    failure_message = 'Исправьте ошибки формы!'

    if request.method == 'POST' and request.is_ajax():
        # Автоматически пробрасываем юзернейм для определения метки

        username = None

        if request.user:
            username = request.user.get_username()

        data = {'name': username}
        data.update(request.POST.dict())

        form = LabelForm(data, request.FILES)

        if form.is_valid():
            label = form.save()
            images = request.FILES.getlist('images')
            Image.objects.bulk_create(
                Image(label=label, image=img) for img in images
            )

            response = JsonResponse({
                'message': success_message
            })
        else:
            response = JsonResponse({
                'message': failure_message,
                'errors': form.errors.as_text_by_key()
            }, status=400)

        return response


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
