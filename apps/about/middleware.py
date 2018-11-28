import os

from django.conf import settings


class AboutPicsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/about/':
            about_pics = os.listdir(
                os.path.join(settings.STATICFILES_DIRS[0], "img/about"))
            request.about_pics = about_pics
        return self.get_response(request)
