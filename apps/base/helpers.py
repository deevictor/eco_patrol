import glob
import os

from django.conf import settings


def list_pics(folder):
    """
    Функция возвращающая список картинок в указанной папке
    :return: Списк вида ['имена файлов в папке', ...]
    :rtype: list

    """
    extensions = ["*.png", "*.jpg", "*.jpeg", ]
    pics_list = []
    for ext in extensions:
        img_path = glob.glob(
            os.path.join(
                settings.STATICFILES_DIRS[0],
                folder + os.sep) + ext
        )
        pics_list.extend(img_path)
        pics_list = [os.path.basename(pic) for pic in pics_list]

    return pics_list
