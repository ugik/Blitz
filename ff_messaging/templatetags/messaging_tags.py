from django import template
register = template.Library()
from ff_messaging.models import UserThread

def num_unread_threads(u):
    ct = 0
    user_threads = UserThread.objects.filter(user=u)
    for user_thread in user_threads:
        if user_thread.is_unread():
            ct += 1
    return ct

num_unread_threads = register.filter('numunreadthreads', num_unread_threads)