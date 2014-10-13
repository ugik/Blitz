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
from base.models import Client, Trainer, TrainerAlert, BlitzMember
from base.alerts import create_alerts_for_day
from datetime import date, timedelta

import datetime


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

@periodic_task(run_every=crontab(hour="*/23", minute="3", day_of_week="*"))  
def usage_digest():
    from django.core.mail import EmailMultiAlternatives
    from django.utils.timezone import now as timezone_now, get_current_timezone as current_tz
    from pytz import timezone

    days = 0
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

    template_html = 'usage_email.html'
    template_text = 'usage_email.txt'

    to = 'georgek@gmail.com'
    from_email = settings.DEFAULT_FROM_EMAIL           
    subject = "Usage Digest"

    text_content = render_to_string(template_text, {'days':days, 'trainers':trainers, 'login_users':login_users, 'members':members, 'MRR':MRR})
    html_content = render_to_string(template_html, {'days':days, 'trainers':trainers, 'login_users':login_users, 'members':members, 'MRR':MRR})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@periodic_task(run_every=crontab(hour="1", minute="1", day_of_week="*"))  
def process_payments():
    email_test()
    pass
# for each client with recurring chargesettings: process recurring charge, handle errors



