from django.conf import settings


def about_pics(request):
    """
    Добавляет в контекст ABOUT_PICS_FOLDER из настроек

    """
    return {'ABOUT_PICS_FOLDER': settings.ABOUT_PICS_FOLDER}
