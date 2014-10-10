from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

SOURCE_EMAIL = 'robot@blitz.us'

def new_child_comment(user, commenter):

    from_email, to = SOURCE_EMAIL, user.email
    subject = "%s replied to your comment on Blitz.us" % commenter.display_name

    text_content = render_to_string('emails/new_child_comment.txt', { 'commenter': commenter } )
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def gym_session_comment(user, commenter):

    from_email, to = SOURCE_EMAIL, user.email
    subject = "%s commented on your lift on Blitz.us" % commenter.display_name

    text_content = render_to_string('emails/gym_session_comment.txt', { 'commenter': commenter } )
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def signup_confirmation(client):

    from_email, to = SOURCE_EMAIL, client.user.email
    subject = "Welcome to Blitz.us!"

    text_content = render_to_string('emails/signup_confirmation.txt', {
        'client': client,
        'blitz': client.get_blitz(),
    })
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def client_invite(trainer, client_email, invite_url):

    from_email, to = SOURCE_EMAIL, client_email
    subject = "Invitation to Blitz.us!"

    text_content = render_to_string('emails/client_invitation.txt', {
        'client': client_email,
        'trainer': trainer,
        'invite_url': invite_url,
    })
    send_mail(subject, text_content, from_email, [to], fail_silently=True)


def forgot_password(user):

    from_email, to = SOURCE_EMAIL, user.email
    subject = "Reset your Blitz.us Password"

    reset_link = settings.SITE_URL + '/reset-password?token=' + user.forgot_password_token

    text_content = render_to_string('emails/forgot_password.txt', {
        'user': user,
        'reset_link': reset_link
    })
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def message_received(user, message):

    from_email, to = SOURCE_EMAIL, user.email
    subject = "New Message on Blitz.us"

    text_content = render_to_string('emails/message_received.txt', {
        'user': user,
        'message': message,
    })
    send_mail(subject, text_content, from_email, [to], fail_silently=True)
