import os
import datetime

BASE_URL = "localhost:8888/"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_LOG = os.path.abspath(os.path.dirname(__file__)) + '/email_log.txt'
USER_ERROR_LOG = os.path.abspath(os.path.dirname(__file__)) + '/email_log.txt'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

STRIPE_PUBLISHABLE_KEY = "pk_test_GNaBSGoHDthi86RxOdzFPuGN "
STRIPE_SECRET_KEY = "sk_test_1E3ZsZbKro2jHUG4Gauqb56T"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.dirname(__file__)) + '/database.sqlite',
    }
}

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'staticfiles'),
)

STATIC_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/collected_static'
