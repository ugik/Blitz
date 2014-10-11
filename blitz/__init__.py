from __future__ import absolute_import
from django.conf import settings

if not settings.DEBUG or True:
    from .celery import app as celery_app
