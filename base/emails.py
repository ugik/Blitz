from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.MIMEImage import MIMEImage

from django.contrib.auth.models import User
from django.db.models import Q
from base.models import Client, Trainer, TrainerAlert, BlitzMember
from workouts.models import WorkoutPlan
from datetime import date, timedelta

import os

SOURCE_EMAIL = 'team@blitz.us'
SPOTTER_EMAIL = 'spotters@blitz.us'

# email wrapper, note parameters: images[] context{}
def send_email(from_email, to_email, subject, text_template, html_template, context, images=[], dirs=[], override=None):  

#    silent = False if settings.DEBUG else True
    silent = True

    if len(images) == 0:
        images = ['emailheader.png']
        dirs = [os.path.join(getattr(settings, 'STATIC_ROOT'), 'images/')]
    else:
        images += ['emailheader.png']
        dirs += [os.path.join(getattr(settings, 'STATIC_ROOT'), 'images/')]

    html_content = render_to_string(html_template, context)
    text_content = render_to_string(text_template, context)
    if override:  # OVERRIDE EMAIL_TO
        to_email = override
    if isinstance(to_email, list):
        msg = EmailMultiAlternatives(subject, text_content, 
                                     from_email, to_email, bcc=[from_email])
    else:
        msg = EmailMultiAlternatives(subject, text_content, 
                                     from_email, [to_email], bcc=[from_email])

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
#    text_content = render_to_string('emails/gym_session_comment.txt', { 'commenter': commenter } )
#    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def signup_confirmation(client):

    from_email, to_email = SOURCE_EMAIL, client.user.email
    subject = "Welcome to Blitz.us!"

    text_template = 'emails/signup_confirmation.txt'
    html_template = 'emails/signup_confirmation.html'
    context = { 'client': client, 'blitz': client.get_blitz() }
    send_email(from_email, to_email, subject, text_template, html_template, context )
#    text_content = render_to_string('emails/signup_confirmation.txt', {
#        'client': client,
#        'blitz': client.get_blitz(),
#    })
#    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def client_invite(trainer, client_email, invite_url):

    from_email, to_email = SOURCE_EMAIL, client_email
    subject = "Invitation to Blitz.us!"

    text_template = 'emails/client_invitation.txt'
    html_template = 'emails/client_invitation.html'
    context = { 'client': client_email, 'trainer': trainer, 'invite_url': invite_url }
    send_email(from_email, to_email, subject, text_template, html_template, context )

#    text_content = render_to_string('emails/client_invitation.txt', {
#        'client': client_email,
#        'trainer': trainer,
#        'invite_url': invite_url,
#    })
#    send_mail(subject, text_content, from_email, [to], fail_silently=True)


def forgot_password(user):

    from_email, to_email = SOURCE_EMAIL, user.email
    subject = "Reset your Blitz.us Password"

    reset_link = settings.SITE_URL + '/reset-password?token=' + user.forgot_password_token
    text_template = 'emails/forgot_password.txt'
    html_template = 'emails/forgot_password.html'
    context = { 'user': user, 'reset_link': reset_link }
    send_email(from_email, to_email, subject, text_template, html_template, context )

#    text_content = render_to_string('emails/forgot_password.txt', {
#        'user': user,
#        'reset_link': reset_link
#    })
#    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def message_received(user, message):

    from_email, to_email = SOURCE_EMAIL, user.email
    subject = "New Message on Blitz.us"

    text_template = 'emails/message_received.txt'
    html_template = 'emails/message_received.html'
    context = { 'user': user, 'message': message }
    send_email(from_email, to_email, subject, text_template, html_template, context )

#    text_content = render_to_string('emails/message_received.txt', {
#        'user': user,
#        'message': message,
#    })
#    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def email_spotter_program_edit(pk, message):
    workoutplan = WorkoutPlan.objects.filter(pk=int(pk))
    if workoutplan:
        from_email, to_email = SOURCE_EMAIL, SPOTTER_EMAIL
        subject = "Program Edit ask from %s" % workoutplan[0].trainer.name

        text_template = 'emails/program_edit.txt'
        html_template = 'emails/program_edit.html'
        context = { 'workoutplan': workoutplan[0], 'message': message }
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


def email_tests():
    from base.models import User, Client, Trainer, Comment
    from ff_messaging.models import Message
    user = User.objects.get(pk=1)
    client = Client.objects.get(pk=1)
    trainer = Trainer.objects.get(pk=1)
    message = Message.objects.get(pk=1)
    comment = Comment.objects.get(pk=1)
    client_invite(trainer, 'georgek@gmail.com', 'program')
    signup_confirmation(client)
    message_received(user, message)
    forgot_password(user)
    gym_session_comment(user, user, comment)
    new_child_comment(user, user, comment)
    email_spotter_program_edit(1, 'spotter email test')


