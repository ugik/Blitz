from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from email.MIMEImage import MIMEImage

from django.contrib.auth.models import User
from django.db.models import Q
from base.models import Client, Trainer, TrainerAlert, BlitzMember, user_display_name
from workouts.models import WorkoutPlan
from spotter.utils import balance

from datetime import date, timedelta
import datetime as dt

import os

SOURCE_EMAIL = 'team@blitz.us'
SPOTTER_EMAIL = 'spotters@blitz.us'
EXAMPLE_EMAILS = False

# email wrapper, note parameters: images[] context{}
def send_email(from_email, to_email, subject, text_template, html_template, context, images=[], dirs=[], override=None, cc_mail=[], trainer=None):  

    silent = False if settings.DEBUG else True

    # don't send emails to @example.com addresses
    if isinstance(to_email, list):
        if [i for i in to_email if 'example.com' in i]:
            if not EXAMPLE_EMAILS:
                print '* @example.com address, no email sent'
                return
    else:
        if 'example.com' in to_email:
            if not EXAMPLE_EMAILS:
                print '* @example.com address, no email sent'
                return

    if len(images) == 0:
        images = ['emailheader.png']
        dirs = [os.path.join(getattr(settings, 'STATIC_ROOT'), 'images/')]
    else:
        images += ['emailheader.png']
        dirs += [os.path.join(getattr(settings, 'STATIC_ROOT'), 'images/')]

    if trainer:    # insert trainer headshot where necessary
        if trainer.headshot:
            headshot = str(trainer.headshot)
            if '/' in headshot:
                images += [headshot[headshot.rfind('/')+1:]]
                dirs += [os.path.join(getattr(settings, 'MEDIA_ROOT'), 'headshots/')]

    html_content = render_to_string(html_template, context)
    text_content = render_to_string(text_template, context)
    if override:  # OVERRIDE EMAIL_TO
        to_email = override
    if isinstance(to_email, list):
        msg = EmailMultiAlternatives(subject, text_content, 
                                     from_email, to_email, cc=cc_mail, bcc=[from_email])
    else:
        msg = EmailMultiAlternatives(subject, text_content, 
                                     from_email, [to_email], cc=cc_mail, bcc=[from_email])

    msg.attach_alternative(html_content, "text/html")
    msg.mixed_subtype = 'related'

    for index, f in enumerate(images):
        fp = open(os.path.join(dirs[index], f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        msg.attach(msg_img)

    msg.send(fail_silently=silent)


def new_child_comment(user, commenter, comment):

    from_email, to_email = SOURCE_EMAIL, user.email
    subject = "%s replied to your comment on Blitz.us" % commenter.display_name

    text_template = 'emails/new_child_comment.txt'
    html_template = 'emails/new_child_comment.html'
    context = { 'commenter': commenter, 'comment': comment  }
    send_email(from_email, to_email, subject, text_template, html_template, context )
#    text_content = render_to_string('emails/new_child_comment.txt', { 'commenter': commenter } )
#    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def gym_session_comment(user, commenter, comment):

    from_email, to_email = SOURCE_EMAIL, user.email
    subject = "%s commented on your lift on Blitz.us" % commenter.display_name

    text_template = 'emails/gym_session_comment.txt'
    html_template = 'emails/gym_session_comment.html'
    context = { 'commenter': commenter, 'comment': comment  }
    send_email(from_email, to_email, subject, text_template, html_template, context )

def signup_confirmation(client, trainer):

    from_email, to_email = SOURCE_EMAIL, client.user.email
    subject = "Welcome to Blitz.us!"

    if dt.datetime.now().date() > client.get_blitz().begin_date:   # blitz has already started
        begins = 'began'   # past tense
        in_meantime = None
    else:
        begins = 'begins'
        in_meantime = True

    text_template = 'emails/signup_confirmation.txt'
    html_template = 'emails/signup_confirmation.html'
    context = { 'client': client, 'blitz': client.get_blitz(), 'begins': begins, 'in_meantime': in_meantime }

    send_email(from_email, to_email, subject, text_template, html_template, context,
               cc_mail=[trainer.user.email] )

def client_invite(trainer, client_email, invite_url, blitz=None):

    from_email, to_email = SOURCE_EMAIL, client_email
    subject = "Invitation for training with %s" % trainer.name 

    text_template = 'emails/client_invitation.txt'
    html_template = 'emails/client_invitation.html'

    headshot_file = str(trainer.headshot)
    headshot = headshot_file[headshot_file.rfind('/')+1:] if '/' in headshot_file else None

    context = { 'client': client_email, 'trainer': trainer, 'invite_url': invite_url, 'blitz': blitz, 'headshot': headshot }
    send_email(from_email, to_email, subject, text_template, html_template, context, trainer=trainer, cc_mail=[trainer.user.email])


def forgot_password(user):

    from_email, to_email = SOURCE_EMAIL, user.email
    subject = "Reset your Blitz.us Password"

    reset_link = 'https://' + settings.SITE_URL + '/reset-password?token=' + user.forgot_password_token
    text_template = 'emails/forgot_password.txt'
    html_template = 'emails/forgot_password.html'
    context = { 'user': user, 'reset_link': reset_link }
    send_email(from_email, to_email, subject, text_template, html_template, context )

def message_received(user, message):

    from_email, to_email = SOURCE_EMAIL, user.email
    subject = "New Message on Blitz.us"

    text_template = 'emails/message_received.txt'
    html_template = 'emails/message_received.html'
    context = { 'user': user, 'message': message }
    send_email(from_email, to_email, subject, text_template, html_template, context )

def program_start(client):

    from_email, to_email = SOURCE_EMAIL, client.user.email
    subject = "Your Blitz.us program begins today!"

    text_template = 'emails/program_begins_today.txt'
    html_template = 'emails/program_begins_today.html'
    context = { 'client': client }
    send_email(from_email, to_email, subject, text_template, html_template, context )

def email_spotter_program_upload(trainer, document):
    from_email, to_email = SOURCE_EMAIL, SPOTTER_EMAIL
    text_template = 'emails/program_upload.txt'
    html_template = 'emails/program_upload.html'

    if trainer:
        subject = "Program upload from %s" % trainer.name
        context = { 'url': document, 'trainer': trainer }
        send_email(from_email, to_email, subject, text_template, html_template, context )


def email_spotter_program_edit(pk, message):
    from_email, to_email = SOURCE_EMAIL, SPOTTER_EMAIL
    text_template = 'emails/program_edit.txt'
    html_template = 'emails/program_edit.html'

    if pk:
        workoutplan = WorkoutPlan.objects.filter(pk=int(pk))
        if workoutplan:
            subject = "Program Edit ask from %s" % workoutplan[0].trainer.name
            context = { 'workoutplan': workoutplan[0], 'message': message }
            send_email(from_email, to_email, subject, text_template, html_template, context )
    else:
        subject = "Program Edit ask"
        context = { 'message': message }
        send_email(from_email, to_email, subject, text_template, html_template, context )


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
    revenue = 0
    for payer in paying_clients:
        if payer.blitzmember_set.all()[0].price:
            revenue += float(payer.blitzmember_set.all()[0].price)

    revenue = float(revenue * 0.12)

    users = User.objects.all()
    login_users = []
    for user in users:
        if timezone.normalize(user.last_login).date() >= startdate:
            user.username = user_display_name(user)
            login_users.append(user)

    f = open('/etc/hosts', 'r')  # grab host and ip address
    lines = [line.strip() for line in f]
    f.close()

    template_html = 'usage_email.html'
    template_text = 'usage_email.txt'
    context = {'days':days+1, 'trainers':trainers, 'login_users':login_users, 'members':members,     
               'revenue':revenue, 'hosts':lines[0]}
    to_mail = ['georgek@gmail.com']
    from_mail = settings.DEFAULT_FROM_EMAIL           
    subject = "Usage Digest"

    send_email(from_mail, to_mail, subject, template_text, template_html, context)

def payment_digest(test=None):

    context = balance(charge=True, test=test)
    if len(context['clients']) == 0:
        return
    
    template_html = 'emails/payments_digest.html'
    template_text = 'emails/payments_digest.txt'
    to_mail = ['georgek@gmail.com']
    from_mail = settings.DEFAULT_FROM_EMAIL           
    subject = "Payments Digest"

    send_email(from_mail, to_mail, subject, template_text, template_html, context)


def usage_trainer(trainer):
    from django.utils.timezone import now as timezone_now, get_current_timezone as current_tz
    from pytz import timezone
    LAGGARD_DAYS = 7

    timezone = current_tz()
    days = 7
    startdate = date.today() - timedelta(days = days)
    enddate = date.today() - timedelta(days=0)
    laggard = date.today() - timedelta(days = days + LAGGARD_DAYS)    # laggard users

    users = []
    clients = Client.objects.all()
    for client in clients:
        if not client.user.is_trainer and client.get_blitz() and client.get_blitz().trainer == trainer:
            users.append(client.user)

    if not users:
        return

    login_users = []
    laggard_users = []
    inactive_users = []

    for user in users:
        if timezone.normalize(user.last_login).date() >= startdate:
            user.username = user_display_name(user)    # username will hold the client/trainer name
            login_users.append(user)
    for user in users:
        # show the trainer users that are laggards but still 'active'
        if timezone.normalize(user.last_login).date() < startdate and timezone.normalize(user.last_login).date() >= laggard:
            user.username = user_display_name(user)
            laggard_users.append(user)
    for user in users:
        # show the trainer users that are laggards but still 'active'
        if timezone.normalize(user.last_login).date() < laggard:
            user.username = user_display_name(user)
            inactive_users.append(user)

    if not login_users and not laggard_users:
        return

    template_html = 'usage_email.html'
    template_text = 'usage_email.txt'
    context = {'days':days, 'trainer':trainer, 'login_users':login_users,
               'laggard_users':laggard_users, 'inactive_users':inactive_users }
    to_mail = [trainer.user.email]

    from_mail = settings.DEFAULT_FROM_EMAIL           
    subject = "Usage Digest"

    send_email(from_mail, to_mail, subject, template_text, template_html, context)

def program_loaded(plan_name, trainer_id):

    trainer = get_object_or_404(Trainer, id=int(trainer_id))
    from_email, to_email = SOURCE_EMAIL, trainer.user.email
    subject = "Your workout program is ready to go!"

    text_template = 'emails/program_loaded.txt'
    html_template = 'emails/program_loaded.html'
    context = { 'trainer': trainer, 'plan_name': plan_name }
    send_email(from_email, to_email, subject, text_template, html_template, context,
               cc_mail=[] )

def program_assigned(workoutplan, blitz):

    trainer = blitz.trainer
    from_email, to_email = SOURCE_EMAIL, trainer.user.email
    subject = "Workout program has been assigned"

    text_template = 'emails/program_assigned.txt'
    html_template = 'emails/program_assigned.html'
    context = { 'trainer': trainer, 'workoutplan': workoutplan, 'blitz': blitz }
    send_email(from_email, to_email, subject, text_template, html_template, context,
               cc_mail=[] )

def email_tests():
    from base.models import User, Client, Trainer, Blitz, Comment
    from workouts.models import WorkoutPlan
    from ff_messaging.models import Message
    user = User.objects.get(pk=3)
    client = Client.objects.get(pk=1)
    trainer = Trainer.objects.get(pk=6)
    message = Message.objects.all()[0]
    comment = Comment.objects.all()[0]
    workoutplan = WorkoutPlan.objects.get(pk=1)
    blitz = Blitz.objects.get(pk=1)
    client_invite(trainer, 'georgek@gmail.com', 'program')
    signup_confirmation(client, trainer)
    message_received(user, message)
    forgot_password(user)
    gym_session_comment(user, user, comment)
    new_child_comment(user, user, comment)
    email_spotter_program_edit(1, 'spotter email test')
    program_loaded(workoutplan.name, trainer.id)
    program_assigned(workoutplan, blitz)
    usage_trainer(trainer)



