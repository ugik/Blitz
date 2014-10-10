import os, site, sys

#virtualEnv pointer
#site.addsitedir('/usr/local/virtualenvs/MYAPP-VIRTUALENV/lib/python2.7/site-pa$

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))
sys.path.append('/home/ubuntu/Blitz')

os.environ["DJANGO_SETTINGS_MODULE"] = 'blitz.settings'

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

env_variables_to_pass = ['EMAIL_PASSWORD', ]
def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)

#####---- newer Django versions
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

#activate_this = '/var/www/michel/testenv/env/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))
#http://stackoverflow.com/questions/9016504/apache-setenv-not-working-as-expected-with-mod-wsgi

#http://ericplumb.com/blog/passing-apache-environment-variables-to-django-via-mod_wsgi.html

