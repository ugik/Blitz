from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now as timezone_now

import random
import string

class Thread(models.Model):

    users = models.ManyToManyField(User, through='UserThread')
    urlkey = models.SlugField(max_length=12, default='')
    last_message_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.urlkey == "":
            self.urlkey = ''.join(random.choice(string.digits) for x in range(10))
        super(Thread, self).save(*args, **kwargs)

    def messages(self):
        return self.message_set.all().order_by('-date_sent')

    def last_received_message_for_user(self, user):
        for m in self.messages():
            if m.sender != user:
                return m.date_sent
        return None

class UserThread(models.Model):

    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    last_read_date = models.DateTimeField(null=True, blank=True)

    def other_users(self):
        return self.thread.users.exclude(pk=self.user.pk)

    def other_user(self):
        if len(self.thread.users.exclude(pk=self.user.pk)) > 0:
            return self.thread.users.exclude(pk=self.user.pk)[0]
        else:
            return None

    def is_unread(self):
        if self.last_read_date is None:
            return True
        last_message_date = self.thread.last_received_message_for_user(self.user)
        if last_message_date is None:
            return False
        return last_message_date > self.last_read_date

class Message(models.Model):

    thread = models.ForeignKey(Thread)
    sender = models.ForeignKey(User, null=True)
    content = models.TextField(default="", blank=True)
    date_sent = models.DateTimeField()
