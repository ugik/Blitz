from __future__ import absolute_import

from celery import Celery
from celery import shared_task

from celery import task
from celery.schedules import crontab
from celery.decorators import periodic_task  
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.utils.timezone import now as timezone_now
from django.conf import settings

from django.contrib.auth.models import User
from django.db.models import Q
from base.models import Client, Trainer, TrainerAlert, BlitzMember
from base.alerts import create_alerts_for_day
from base.emails import send_email, usage_digest
from datetime import date, timedelta

import datetime
import os

# celery periodic tasks http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab  


@periodic_task(run_every=crontab(hour="*", minute="59", day_of_week="*"))  
def backup():
    # check to make sure database is up and real
    c = Client.objects.all()
    if len(c) > 0:
        os.system("bash ~/Blitz/backup.sh")

@periodic_task(run_every=crontab(hour="23", minute="59", day_of_week="*"))  
def usage_digest(): 
    usage_digest()

#@periodic_task(run_every=crontab(hour="23", minute="59", day_of_week="*"))  
#def email_test(): 
#    send_mail('Celery email test', 'Daily test email celery', 'team@blitz.us', ['georgek@gmail.com'])

@periodic_task(run_every=crontab(hour="*", minute="1", day_of_week="*"))  
def trainer_alerts():
    for client in Client.objects.all():
        blitz = client.get_blitz()
        if True or client.current_datetime().hour != settings.ALERTS_HOUR:
            continue
        if blitz is None:
            continue
        if not blitz.in_progress(client.get_timezone()):
            continue

        yesterday = client.current_datetime().date() + datetime.timedelta(days=-1)
        create_alerts_for_day(client, yesterday)

@periodic_task(run_every=crontab(hour="*", minute="2", day_of_week="*"))  
def client_morning_notifications():
    for client in Client.objects.all():

        blitz = client.get_blitz()
        if client.current_datetime().hour != settings.MORNING_NOTIFICATIONS_HOUR:
            continue
        if blitz is None:
            continue

        # plan starts today
        if blitz.begin_date == client.current_datetime().date():
            from_email, to = "team@blitz.us", client.user.email
            subject = "Your Blitz.us program begins today!"

            text_content = render_to_string('emails/program_begins_today.txt', {
                'client': client,
                'blitz': blitz,
            } )
            send_mail(subject, text_content, from_email, [to], fail_silently=True)



