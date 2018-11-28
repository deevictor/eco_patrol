from mezzanine.pages.page_processors import processor_for

from label.forms import LabelForm
from label.models import Category, Label


@processor_for('/')
def index(request, page):
    """"
    Отображает главную страницу.
    Контекст:
    form_label (form): Форма для отправки меток с карты на сайт
    form_user (form): Форма для регистрации пользователей
    login_form (form): Форма для авторизации пользователей
    body_class (str): Глобальный класс css для всей страницы
    """
    try:
        balloon = Label.objects.get(id=request.GET.get("id_balloon", 0))
    except Label.DoesNotExist:
        balloon = None

    top_labels = Label.objects.filter(in_top=True)
    images = []

    for label in top_labels:
        image = label.image_set.first()
        if image:
            images.append({
                'image': image,
                'label': label
            })

    return {
        'form_label': LabelForm(),
        'body_class': 'page-index',
        'categories': Category.objects.all(),
        'balloon': balloon,
        'label_gallery': images
    }
