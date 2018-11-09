Описание пакета


По-умолчанию папки static и media размещаются в папке
<виртуальное окружение>/var. Для изменения этого пути необходимо добавить в
окружение переменную LOCAL_FILES_DIR, содержащую новый путь разменения static и
media


Проверка состояния кода


isort --settings-path isort.cfg -rc ./apps


pylint --rcfile=pylint.rc .
