from __future__ import absolute_import
import os
from datetime import timedelta

ADMINS = (
    ('GK', 'georgek@gmail.com'),
#    ('Chris York', 'chris@therealchrisyork.com'),
)

MANAGERS = ADMINS

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'data',
        'USER' : 'django',
        'PASSWORD' : 'django',
        },
    }


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SITE_URL = 'Blitz.us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'usermedia')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'staticfiles'),
)

# ./manage.py collectstatic destination
STATIC_ROOT = (
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'collected_static')
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1(=g!@qyc)&b(v46g11$f1=3a#0#f-6_ti8k4og@wo5(8buk8='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'blitz.urls'
APPEND_SLASH = False

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'blitz.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
)

INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    'django.contrib.admindocs',

    'south',
    'django_extensions',
    'tastypie',
    'djcelery',

    'base',
    'workouts',
    'ff_messaging',
    'spotter',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_URL = '/login'
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data')
TEST_MEDIA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../testmedia')

try:
    from .local_settings import *
except:
    pass

# gmail SMTP setup
# for local server, export var in ~/.bashrc
# for apache server, SetEnv var in /etc/apache2/httpd.conf
if 'EMAIL_PASSWORD' in os.environ:
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
else:
    print "NEED TO SET EMAIL_PASSWORD"

EMAIL_HOST = 'smtp.blitz.us'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'team@blitz.us'
DEFAULT_FROM_EMAIL = 'team@blitz.us'
SERVER_EMAIL = 'team@blitz.us'

import djcelery  
djcelery.setup_loader()  
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_BEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TIMEZONE = 'US/Pacific'
ALERTS_HOUR = 23
MORNING_NOTIFICATIONS_HOUR = 5

import balanced
# Production settings for Balanced Marketplace
balanced.configure('ak-test-2HbxysbHinoGa4nnmnLz63SluBiYiUQCV')
BALANCED_MARKETPLACE_URI = '/v1/marketplaces/TEST-MP1tHThD8oovCyo9YnXXWImY'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",

    "base.context_processors.custom_processor",
)
