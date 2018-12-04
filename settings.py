import importlib
import os
import sys

from django.conf.global_settings import *  # @UnusedWildImport

try:
    virtualenv_root = os.environ['VIRTUAL_ENV']
except KeyError:
    sys.stderr.write('Error: virtualenv does not activated.\n')
    sys.exit(1)

VAR_ROOT = os.path.join(virtualenv_root, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = False

SECRET_KEY = ''
NEVERCACHE_KEY = ''

DEBUG = False

#########
# PATHS #
#########

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = BASE_DIR

PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
PROJECT_APP = os.path.basename(BASE_DIR)
FILE_UPLOAD_PERMISSIONS = 0o644
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

MEDIA_ROOT = os.path.join(VAR_ROOT, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.pages',
    'mezzanine.blog',
    'mezzanine.accounts',
    'sorl.thumbnail',
    'feedback',
    'base',
    'label',
    'user',
    'about',
]

MIDDLEWARE = [
    'mezzanine.core.middleware.UpdateCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',

    'about.middleware.AboutMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
                'about.context_processors.about_pics',
                'mezzanine.conf.context_processors.settings',
                'mezzanine.pages.context_processors.page',

            ],
            'builtins': [
                'mezzanine.template.loader_tags',
            ],
            'loaders': [
                'mezzanine.template.loaders.host_themes.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

AUTH_USER_MODEL = 'user.User'
ACCOUNTS_PROFILE_FORM_CLASS = "user.forms.UserRegisterForm"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

TIME_ZONE = 'Asia/Vladivostok'

LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Russian'),
]
USE_I18N = True

USE_L10N = True

USE_TZ = False

SLUGIFY = 'pytils.translit.slugify'

# Это название сайта в админке, отображающееся
# в шапке админки и в форме логирования
GRAPPELLI_ADMIN_TITLE = 'Конструктор городской среды'

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

AUTHENTICATION_BACKENDS = ('mezzanine.core.auth_backends.MezzanineBackend',
                           'django.contrib.auth.backends.ModelBackend',)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
# FILE_UPLOAD_PERMISSIONS = 0o644


# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    'debug_toolbar',
    'django_extensions',
    'compressor',
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

module_name = 'settings_local'
module_spec = importlib.util.find_spec(module_name)
module = importlib.util.module_from_spec(module_spec)
sys.modules[module_name] = module
exec(open(module.__file__, 'rb').read())

RICHTEXT_ALLOWED_TAGS = (
    'a', 'abbr', 'acronym', 'address', 'area', 'b', 'bdo', 'big',
    'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code',
    'col', 'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt',
    'em', 'fieldset', 'font', 'form', 'figure', 'h1', 'h2', 'h3', 'h4', 'h5',
    'h6', 'hr', 'i', 'img', 'input', 'ins', 'iframe', 'kbd', 'label', 'legend',
    'li', 'map', 'menu', 'ol', 'optgroup', 'option', 'p', 'pre', 'q',
    's', 'section', 'script', 'samp', 'select', 'small', 'span', 'strike',
    'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th',
    'thead', 'tr', 'tt', 'u', 'ul', 'var', 'wbr'
)

RICHTEXT_ALLOWED_ATTRIBUTES = (
    'abbr', 'accept', 'accept-charset', 'accesskey', 'action',
    'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
    'char', 'charoff', 'charset', 'checked', 'cite', 'class', 'clear',
    'cols', 'colspan', 'color', 'compact', 'coords', 'data-tab', 'datetime',
    'dir', 'disabled', 'enctype', 'for', 'frame', 'headers', 'height', 'href',
    'hreflang', 'hspace', 'id', 'ismap', 'label', 'lang', 'longdesc',
    'maxlength', 'media', 'method', 'multiple', 'name', 'nohref',
    'noshade', 'nowrap', 'prompt', 'readonly', 'rel', 'rev', 'rows',
    'rowspan', 'rules', 'scope', 'selected', 'shape', 'size', 'span',
    'src', 'start', 'style', 'summary', 'tabindex', 'target', 'title',
    'type', 'usemap', 'valign', 'value', 'vspace', 'width', 'xml:lang'
)

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'relative_urls': False,
    'language': 'ru',
}

DASHBOARD_TAGS = (
    ("mezzanine_tags.app_list",),
    ("mezzanine_tags.recent_actions",),
    (),
)

ADMIN_MENU_ORDER = (
    (u"Содержимое", (
        "pages.Page",
        (u"Новости", "blog.BlogPost"),
        (u"Медиа-библиотека", "fb_browse"),
        "feedback.Feedback",
    )),
    (u"Пользователи", (
        "user.User",
        "auth.Group",
    )),
    (u"Карта", (
        "label.Category",
        "label.Label",
    )),
    (u"Прочее", (
        "conf.Setting",
        "sites.Site",
    )),
)

PAGE_MENU_TEMPLATES = (
    (1, u'Главное меню', 'pages/menus/header_menu.html'),
)

BLOG_SLUG = "news"

MAX_UPLOAD_SIZE = 104857600
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
SITE_TITLE = 'Экодозор'

# Название папки с картинками для вывода в карусели на странице /about/
# папка должна находится в /static/
ABOUT_PICS_FOLDER = 'img/about/'
