from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import now as timezone_now
from base.utils import get_inboxfeed_html, JSONResponse

import json

from forms import NewMessageForm
from models import Message, Thread, UserThread
from utils import possible_recipients_for_user, get_thread_for_users, create_new_message, thread_exists_for_users

@login_required()
def inbox(request):
    user_threads = UserThread.objects.filter(user=request.user).order_by('-thread__last_message_date')
    possible_recipients = possible_recipients_for_user(request.user)
    try:
        new_message_to_user = request.session.pop('new_message_to_user')
    except KeyError:
        new_message_to_user = None
    return render(request, 'messages/inbox.html', {
        'recipient_names_json': json.dumps([u.display_name for u in possible_recipients]),
        'recipient_map_json': json.dumps({u.display_name: u.pk for u in possible_recipients}),
        'user_threads': user_threads,
        'new_message_to_user': new_message_to_user
    })

@login_required()
def inbox_feed(request):
    user_threads = UserThread.objects.filter(user=request.user).order_by('-thread__last_message_date')
    possible_recipients = possible_recipients_for_user(request.user)
    try:
        new_message_to_user = request.session.pop('new_message_to_user')
    except KeyError:
        new_message_to_user = None

    ret = {
        'html': get_inboxfeed_html(user_threads)
    }
    return JSONResponse(ret)

@login_required()
def new_message(request):
    if request.method == 'GET':
        return inbox(request)
    form = NewMessageForm(request.POST)
    if form.is_valid():
        thread = get_thread_for_users(request.user, form.cleaned_data['to_user'])
        message = create_new_message(thread, request.user, form.cleaned_data['message_content'])
        return redirect('user_thread', urlkey=thread.urlkey)
    else:
        return redirect('/inbox')

@login_required()
def user_thread(request, urlkey):
    thread = get_object_or_404(Thread, urlkey=urlkey)
    current_user_thread = get_object_or_404(UserThread, thread=thread, user=request.user)
    current_user_thread.last_read_date = timezone_now()
    current_user_thread.save()

    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            message = create_new_message(thread, request.user, form.cleaned_data['message_content'])
    else:
        form = NewMessageForm()
    # TODO: authX - can user see thread
    user_threads = UserThread.objects.filter(user=request.user).order_by('-thread__last_message_date')
    return render(request, 'messages/thread.html', {
        'thread': thread,
        'current_user_thread': current_user_thread,
        'user_threads': user_threads,
        'form': form,
    })


@login_required()
def new_message_to_user(request, pk):
    to_user = get_object_or_404(User, pk=int(pk))
    if thread_exists_for_users(to_user, request.user):
        print to_user.display_name, request.user.display_name
        thread = get_thread_for_users(to_user, request.user)
        return redirect('user_thread', urlkey=thread.urlkey)
    else:
        request.session['new_message_to_user'] = to_user
        return redirect('new_message')

@login_required()
@csrf_exempt
def send_message_to_user(request, pk):
    to_user = get_object_or_404(User, pk=int(pk))

    print to_user.display_name, request.user.display_name
    thread = get_thread_for_users(request.user, to_user)
    message_content = str( request.GET.get('message_content', '') )
    message = create_new_message(thread, request.user, message_content)

    return JSONResponse({
        'from_user': request.user,
        'to_user': to_user,
        'message_content': message_content
    })
    
