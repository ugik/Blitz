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
from base.emails import send_email
from datetime import date, timedelta

import datetime
import os

# celery periodic tasks http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab  

@task()
def email_test(): 
    send_mail('Celery email test', 'Daily test email celery', 'robot@blitz.us', ['georgek@gmail.com'])


@periodic_task(run_every=crontab(hour="*/1", minute="1", day_of_week="*"))  
def trainer_alerts():
    for client in Client.objects.all():
        blitz = client.get_blitz()
        if client.current_datetime().hour != settings.ALERTS_HOUR:
            continue
        if blitz is None:
            continue
        if not blitz.in_progress(client.get_timezone()):
            continue

        yesterday = client.current_datetime().date() + datetime.timedelta(days=-1)
        create_alerts_for_day(client, yesterday)

@periodic_task(run_every=crontab(hour="*/1", minute="2", day_of_week="*"))  
def client_morning_notifications():
    for client in Client.objects.all():

        blitz = client.get_blitz()
        if client.current_datetime().hour != settings.MORNING_NOTIFICATIONS_HOUR:
            continue
        if blitz is None:
            continue

        # plan starts today
        if blitz.begin_date == client.current_datetime().date():
            from_email, to = "robot@blitz.us", client.user.email
            subject = "Your Blitz.us program begins today!"

            text_content = render_to_string('emails/program_begins_today.txt', {
                'client': client,
                'blitz': blitz,
            } )
            send_mail(subject, text_content, from_email, [to], fail_silently=True)

@periodic_task(run_every=crontab(hour="1", minute="3", day_of_week="*"))  
def usage_digest(days=0):
    from django.core.mail import EmailMultiAlternatives
    from django.utils.timezone import now as timezone_now, get_current_timezone as current_tz
    from pytz import timezone

    timezone = current_tz()
    startdate = date.today() - timedelta(days = days)

    enddate = date.today() - timedelta(days=0)
    trainers = Trainer.objects.filter(date_created__range=[startdate, enddate])
    members = BlitzMember.objects.filter(date_created__range=[startdate, enddate])

    # get clients with CC on file
    paying_clients = Client.objects.filter(~Q(balanced_account_uri = ''))
    MRR = 0
    for payer in paying_clients:
        if payer.blitzmember_set:
            # recurring monthly charge
            if payer.blitzmember_set.all()[0].blitz.recurring:
                MRR += float(payer.blitzmember_set.all()[0].blitz.price)
            # monthly charge for non-recurring blitz
            else: 
                MRR += float(payer.blitzmember_set.all()[0].blitz.price / payer.blitzmember_set.all()[0].blitz.num_weeks() * 4)

    users = User.objects.all()
    login_users = []
    for user in users:
        if timezone.normalize(user.last_login).date() >= startdate:
            login_users.append(user)

    f = open('/etc/hosts', 'r')  # grab host and ip address
    lines = [line.strip() for line in f]
    f.close()

    template_html = 'usage_email.html'
    template_text = 'usage_email.txt'
    context = {'days':days, 'trainers':trainers, 'login_users':login_users, 'members':members,     
               'MRR':MRR, 'hosts':lines[0]}
    to_mail = ['georgek@gmail.com']
    from_mail = settings.DEFAULT_FROM_EMAIL           
    subject = "Usage Digest"

    send_email(from_mail, to_mail, subject, template_text, template_html, context)


@periodic_task(run_every=crontab(hour="1", minute="1", day_of_week="*"))  
def process_payments():
    pass
# for each client with recurring chargesettings: process recurring charge, handle errors



