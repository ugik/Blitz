from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.utils.timezone import now as timezone_now
from django.conf import settings

from base.models import Client, Trainer, TrainerAlert
from base.alerts import create_alerts_for_day

logger = get_task_logger(__name__)

# http://celery.readthedocs.org/en/latest/reference/celery.schedules.html
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    logger.info("Task finished: result = %i" % result)


@periodic_task(run_every=(crontab(hour="24", minute="*", day_of_week="*")))
def trainer_alerts():
    for client in Client.objects.all():
        blitz = client.get_blitz()

        if blitz is None:
            continue
        if not blitz.in_progress(client.get_timezone()):
            continue

        yesterday = client.current_datetime().date() + datetime.timedelta(days=-1)
        create_alerts_for_day(client, yesterday)


@periodic_task(run_every=(crontab(hour="23", minute="*", day_of_week="*")))
def client_morning_notifications():
    for client in Client.objects.all():

        blitz = client.get_blitz()

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

@task()
def email_bt(): 
    send_mail('hi', 'test email celery', 'robot@blitz.us', ['georgek@gmail.com'])

