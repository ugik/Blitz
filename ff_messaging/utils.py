from django.contrib.auth.models import User
from django.utils.timezone import now as timezone_now
from models import Message, Thread, UserThread
from base import emails

def possible_recipients_for_user(user):
    if user.is_trainer:
        users = set()
        for blitz in user.trainer.active_blitzs():
            users = users | set(blitz.active_users())
        return list(users)
    else:
        users = set(user.blitz.active_users())
        users.discard(user)
        return list(users)

def thread_for_users(user1, user2):
    """
    Nothing special about a thread...just a list of messages between these two users
    """
    from1 = list(Message.objects.filter(from_user=user1, to_user=user2))
    from2 = list(Message.objects.filter(from_user=user2, to_user=user1))
    all_messages = sorted(from1 + from2, key=lambda x: x.date_sent)
    return all_messages

def get_thread_for_users(*args):
    """
    Must have at least two *args
    """
    threads = Thread.objects.filter(users=args[0])
    for user in args[1:]:
        threads = threads.filter(users=user)
    if threads.count() > 1:
        raise Exception("More than one thread")
    elif threads.count() == 1:
        return threads[0]
    else:
        thread = Thread.objects.create()
        for user in args:
            UserThread.objects.create(thread=thread, user=user)
        return thread


def thread_exists_for_users(*args):
    """
    Must have at least two *args
    """
    threads = Thread.objects.filter(users=args[0])
    for user in args[1:]:
        threads = threads.filter(users=user)
    if threads.count() > 1:
        raise Exception("More than one thread")
    return threads.count() == 1

def create_new_message(thread, sender, message_content):
    dt = timezone_now()
    message = Message.objects.create(
            thread=thread,
            content=message_content,
            sender=sender,
            date_sent=dt
    )
    thread.last_message_date = dt
    thread.save()
    for user in thread.users.exclude(pk=sender.pk):
        emails.message_received(user, message)
