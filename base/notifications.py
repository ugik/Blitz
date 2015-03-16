from django.core.mail import send_mail
from django.template.loader import render_to_string

SOURCE_EMAIL = 'robot@blitz.us'

def new_child_comment(user, commenter, comment):

    from_email, to = SOURCE_EMAIL, user.email
    subject = "%s replied to your comment on Blitz.us" % commenter.display_name

    text_content = render_to_string('emails/new_child_comment.txt', { 'commenter': commenter, 'comment': comment } )
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def gym_session_comment(user, commenter, comment):
    """
    Send a notification to user that commenter has commented on his/her gym session
    """

    from_email, to = SOURCE_EMAIL, user.email
    subject = "%s commented on your lift on Blitz.us" % commenter.display_name

    text_content = render_to_string('emails/gym_session_comment.txt', { 'commenter': commenter, 'comment': comment } )
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

def checkin_comment(user, commenter, comment):
    """
    Send a notification to user that commenter has commented on his/her checkin
    """

    from_email, to = SOURCE_EMAIL, user.email
    subject = "%s commented on your checkin on Blitz.us" % commenter.display_name

    text_content = render_to_string('emails/checkin_comment.txt', { 'commenter': commenter, 'comment': comment } )
    send_mail(subject, text_content, from_email, [to], fail_silently=True)

