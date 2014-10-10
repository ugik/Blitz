from django import template
register = template.Library()
from django.contrib.contenttypes.models import ContentType
from workouts.models import DAYS_OF_WEEK

import datetime

def key(d, key_name):
    return d[key_name]
key = register.filter('key', key)

def forindex(a, index):
    return a[index]
forindex = register.filter('forindex', forindex)

def content_type_name(model_instance):
    return ContentType.objects.get_for_model(model_instance).name
key = register.filter('content_type_name', content_type_name)

def day_name(day_char):
    return dict(DAYS_OF_WEEK)[day_char]
key = register.filter('day_name', day_name)

def liked_by_user(object, user):
    return object.liked_by_user(user)
key = register.filter('liked_by_user', liked_by_user)

def dayssince(value):
    "Returns number of days between today and value."
    today = datetime.date.today()
    diff  = today - value
    if diff.days > 1:
        return '%s days ago' % diff.days
    elif diff.days == 1:
        return 'yesterday'
    elif diff.days == 0:
        return 'today'
    else:
        # Date is in the future; return formatted date.
        return value.strftime("%B %d, %Y")

def divide(value, arg):
    "Returns numeric value divided by provided arg"
    return float(value)/float(arg)

register.filter('dayssince', dayssince)
register.filter('divide', divide)