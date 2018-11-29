import glob
import os

from django.conf import settings


class PicsMiddleware:
    """
    Добавляет в request словарь названий папок со списками картинок в них

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.pics = self.list_pics()

        return self.get_response(request)

    @staticmethod
    def list_pics():
        """
        Функция возвращающая словарь содержащий файлы во всех указанных в
        настройках папках

        :return: Словарь вида 'название папки': ['имена файлов в папке']
        :rtype: dict

        """
        pics = {}
        extensions = ["*.png", "*.jpg", "*.jpeg", ]

        for folder in settings.PICS_FOLDERS:
            pics_list = []
            for ext in extensions:
                img_path = glob.glob(
                    os.path.join(
                        settings.STATICFILES_DIRS[0], 'img',
                        folder + os.sep) + ext
                )
                pics_list.extend(img_path)
            pics_list = [os.path.basename(pic) for pic in pics_list]
            pics[folder] = pics_list

        return pics
