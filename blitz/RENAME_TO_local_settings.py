import os
import datetime

BASE_URL = "localhost:8888/"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_LOG = os.path.abspath(os.path.dirname(__file__)) + '/email_log.txt'
USER_ERROR_LOG = os.path.abspath(os.path.dirname(__file__)) + '/email_log.txt'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

import balanced
# Test settings for Balanced Marketplace
balanced.configure('ak-test-2HbxysbHinoGa4nnmnLz63SluBiYiUQCV')
BALANCED_MARKETPLACE_URI = '/v1/marketplaces/TEST-MP1tHThD8oovCyo9YnXXWImY'

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
