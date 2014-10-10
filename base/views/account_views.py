from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from base.forms import LoginForm, SetPasswordForm, CreateAccountForm, ForgotPasswordForm, EmailRegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect

from base import emails
from base.models import Trainer, Client
from base.utils import create_trainer
from django.contrib.auth.models import User
from django.core.mail import mail_admins

import random
import string
import re

def login_view(request):

    if "standard" in request.GET:
        return standard_login_view(request)

    error = ""
    form = EmailRegisterForm(request.POST)
    if request.method == 'POST':
        form = EmailRegisterForm(request.POST)
        if form.is_valid():
            email = form.data['email']
            if not re.match(r"^[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+\.[a-zA-Z]{3,}$", email)!=None:
                error = "Invalid email format"
            else:
                if User.objects.filter(email=form.data['email']):
                    error = "Email already registered"
                else:
                    # use trainer as registration store
                    trainer = create_trainer(
                        form.data['email'],
                        form.data['email'],
                        "asdf", None, "gk"
                    )
                    mail_admins('email registration', '%s signed up' % form.data['email'])
                    return render(request, "email_register_done.html", { })

    else:
        form = EmailRegisterForm()

    return render(request, "email_register.html", {
        'form': form, 'error': error
    })


def standard_login_view(request):
    logout(request)

#    import pdb; pdb.set_trace()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            next = request.GET.get('next', '/')
            login(request, form.cleaned_data['user'])
            return redirect(next)

    else:
        form = LoginForm()

    #displays the error but preserves the e-mail address entered
    return render(request, "login.html", {
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect('login_view')

def forgot_password(request):

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            user = User.objects.get(email=email)
            if user.is_trainer:
                profile = user.trainer
            else:
                profile = user.client
            profile.forgot_password_token = "".join([random.choice(string.ascii_letters) for i in range(30)])
            profile.save()
            emails.forgot_password(user)
            return redirect('forgot_password_sent')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {
        'form': form,
    })

def forgot_password_sent(request):

    return render(request, 'forgot_password_sent.html', {
        'email': request.session.get('email')
    })


def reset_password(request):

    if not request.GET.get('token'):
        return HttpResponse('Invalid token')

    try:
        user = Trainer.objects.get(forgot_password_token=request.GET['token']).user
    except ObjectDoesNotExist:
        try:
            user = Client.objects.get(forgot_password_token=request.GET['token']).user
        except ObjectDoesNotExist:
            return HttpResponse('Invalid token')

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()

            if user.is_trainer:
                t = user.trainer
            else:
                t = user.client
            t.forgot_password_token = ""
            t.save()

            u = authenticate(username=user.username, password=form.cleaned_data['password1'])
            print u
            login(request, u)
            return redirect('reset_password_complete')

    else:
        form = SetPasswordForm()

    return render(request, 'reset_password.html', {
        'form': form,
    })

def reset_password_complete(request):

    return render(request, 'reset_password_complete.html', {
    })
