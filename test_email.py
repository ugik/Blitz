from base.emails import send_email
from django.conf import settings
import os

template_html = 'emails/sample_email.html'
template_text = 'emails/sample_email.txt'
context = {'something' : 'foo'}
to_mail = ['georgek@gmail.com']
from_mail = 'team@blitz.us'          
subject = "Usage Digest"
images = ['logo-bp2.png','footer.png']
dirs = [os.path.join(getattr(settings, 'STATIC_ROOT'), 'images/'),
        os.path.join(getattr(settings, 'STATIC_ROOT'), 'images/')]
send_email(from_mail, to_mail, subject, template_text, template_html, context, images, dirs )



