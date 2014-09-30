"""
Django settings for ehf project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '93bx0zs26mpy-4&iuhhhwr2u9t%a(_3*&#6pix_og*=-5t8912'

# Application definition

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'smuggler',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'pagination',
    'chartit',
    'rest_framework',
    'browse',
    'search',
    'analysis',
    'download',
    'about',
    'news',
    'rest',
    'help',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'ehf.urls'

WSGI_APPLICATION = 'ehf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "collectStatic")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
PKL_DIR = os.path.join(MEDIA_ROOT, "pkl")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    #"django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    #"django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_WINDOW = 1
PAGINATION_INVALID_PAGE_RAISES_404 = True

# administrator email address
# ADMIN_EMAIL = "liuyang@bmi.ac.cn"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = '587'
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],

    'PAGINATE_BY': 10
}


GRAPPELLI_ADMIN_TITLE = 'EHFPI Admin'
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_VERSIONS_BASEDIR='_versions/'

SITE_ID = 1
#development server
if socket.gethostname() == 'jacky-PC':
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ehfpi',
            'USER': 'root',
            'PASSWORD': 'mysql',
            'HOST': '',
            'PORT': ''
        }
    }
    URL_PREFIX = '/ehfpi'

else:  #production server
    DEBUG = False
    TEMPLATE_DEBUG = False

    ADMINS = (
    ('Liu Yang', 'liuyang@bmi.ac.cn'),
    )
    ALLOWED_HOSTS = ['127.0.0.1','localhost','biotech.bmi.ac.cn']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ehfpi',
            'USER': 'ehfpi',
            'PASSWORD': '19881010',
            'HOST': '',
            'PORT': ''
        }
    }
    URL_PREFIX = '/ehfpi'