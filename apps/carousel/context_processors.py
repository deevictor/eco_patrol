from django.conf import settings


def carousel_pics(request):
    """
    Добавляет в контекст пути до папок с картинками для карусели из настроек

    """

    pics = {
        'ABOUT_PICS_FOLDER': settings.ABOUT_PICS_FOLDER,
        'BECOME_PICS_FOLDER': settings.BECOME_PICS_FOLDER,
    }

    return pics
