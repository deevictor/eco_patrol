from django.conf import settings

from base.helpers import list_pics


class CarouselMiddleware:
    """
    Добавляет в request список картинок для страниц about и become

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.about_pics = list_pics(settings.ABOUT_PICS_FOLDER)
        request.become_pics = list_pics(settings.BECOME_PICS_FOLDER)

        return self.get_response(request)
