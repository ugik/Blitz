from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404, render_to_response, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import mail_admins
from django.db.models import Q
from django.core.urlresolvers import resolve
from spotter.urls import *

from base.forms import LoginForm, SetPasswordForm, Intro1Form, ProfileURLForm, CreateAccountForm, SubmitPaymentForm, SetMacrosForm, NewTrainerForm, UploadForm, BlitzSetupForm, NewClientForm, ClientSettingsForm, CommentForm, ClientCheckinForm, SalesBlitzForm, SpotterProgramEditForm
from workouts import utils as workout_utils
from base.utils import get_feeditem_html, get_client_summary_html, JSONResponse, grouped_sets_with_user_data, get_lift_history_maxes, create_salespagecontent
from base import utils
from base.emails import client_invite, email_spotter_program_edit

from base.models import Trainer, FeedItem, GymSession, CompletedSet, Comment, CommentLike, Client, Blitz, BlitzInvitation, WorkoutSet, GymSessionLike, TrainerAlert, SalesPageContent, CheckIn, Heading
from workouts.models import WorkoutPlan

from base.templatetags import units_tags
from base import new_content
from base import emails
from base import macro_utils

import datetime, time
import random
import string
import json
import requests
import pytz
import logging
import os 

from cStringIO import StringIO
from PIL import Image
import urllib2

MEDIA_URL = getattr(settings, 'MEDIA_URL')

def domain(request):
    uri = request.build_absolute_uri()   # get full uri
    uri = uri[uri.index('//')+2:]        # remove the http://
    uri = uri[0:uri.index('/')]          # get domain
    return uri

def privacy_policy(request):
    content = render_to_string('privacypolicy.html')
    return render(request, 'legal_page.html', {'legal_content': content})

def terms_of_use(request):
    content = render_to_string('termsofuse.html')
    return render(request, 'legal_page.html', {'legal_content': content})

def all_clients(request):
    if request.user.is_staff:
        clients = Client.objects.all()
    elif request.user.is_trainer:           # show clients for a trainer
        all_clients = Client.objects.all()
        clients = []
        for c in all_clients:
            if c.get_blitz().trainer == request.user.trainer:
                clients.append(c)

    return render(request, 'all_clients.html', {'clients': clients})

def register(request):
    return render(request, 'register.html')

def home(request):

    if request.user.is_authenticated():

        try:
            trainer = request.user.trainer
            return trainer_home(request)
        except ObjectDoesNotExist:
            pass

        try:
            client = request.user.client
            return client_home(request)
        except ObjectDoesNotExist:
            pass

        # handle spotter type users, see spotter app for details
        if request.user._wrapped.username == 'spotter':
#             return spotter_index(request)
            return redirect('spotter_index')

        raise Exception("Invalid user")

    return redirect('login_view')
    #return landing(request)

def landing(request):
    return render(request, 'landing.html', {
    })


def get_pending_documents(path, trainer_pk):
    path = settings.MEDIA_ROOT + path
    doclist = os.listdir(path)
    numdocs = 0
    for doc in doclist:
        if doc.startswith(str(trainer_pk)+'__') and not doc.endswith('.backup'):
            numdocs += 1
    return numdocs

@login_required
def trainer_home(request):

# deal with new trainer with pending documents
    trainer = request.user.trainer
    numdocs = get_pending_documents('/documents', trainer.pk)

# deal with new trainer without blitz but with new program setup
    new_programs = WorkoutPlan.objects.filter(trainer=trainer.pk)
    new_program_name = None
    if new_programs:
        new_program_name = new_programs[0].name

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            new_content.create_new_parent_comment(request.user, 
                      form.cleaned_data['comment'], 
                      timezone_now(),
                      form.cleaned_data['picture'])
        else:
            form = CommentForm()

    return render(request, 'trainer_home.html', {
        'trainer' : trainer,
        'alerts': trainer.get_alerts(),
        'docs' : numdocs,
        'new_programs' : len(new_programs),
        'new_program_name' : new_program_name,
    })


@login_required
def blitz_setup(request):

    trainer = request.user.trainer
    programs = WorkoutPlan.objects.filter(trainer_id = trainer.id)
    if request.method == 'POST':
        form = BlitzSetupForm(request.POST, trainer=trainer)
        errors = []

        if 'title' in form.data:
            title = form.data['title']
            if len(title)<5:
                errors.append("Title too short")
        else:
            errors.append("No title")

        charge = form.data['charge']
        start = form.data['start_day']

        try:
            datetime.datetime.strptime(start, '%Y-%m-%d')
        except ValueError:
            errors.append("Incorrect DATE format, should be YYYY-MM-DD")
        if not charge.isdigit():
            errors.append("CHARGE $ must be number")

#        import pdb; pdb.set_trace()
        if not errors and form.is_valid():
            if 'program' in form.data:
                program = form.data['program']
                plan = WorkoutPlan.objects.filter(name=program)
            else:
                plan = None

            content = create_salespagecontent(form.data['title'], trainer, key=None, title=None)

            if not plan: # blitz w/workoutplan pending
                blitz = Blitz.objects.create(trainer = trainer, begin_date = datetime.datetime.strptime(start, '%Y-%m-%d'))
            else:  # blitz w/workoutplan selected
                blitz = Blitz.objects.create(trainer = trainer, begin_date = datetime.datetime.strptime(start, '%Y-%m-%d'), workout_plan = plan[0])
            blitz.title = form.data['title']
            blitz.sales_page_content = content
            blitz.url_slug = form.data['url_slug']
            blitz.price = charge
            blitz.uses_macros = True
            blitz.macro_strategy = 'M'
            blitz.recurring = False if form.data['blitz_type'] == "GRP" else True
            blitz.provisional = True if blitz.recurring else False
            blitz.save()

            return render_to_response('blitz_setup_done.html', 
                              {'form': form, 'trainer' : trainer}, 
                              RequestContext(request))
        else:

# TODO make sure start_day value shows up in form
            return render_to_response('blitz_setup.html', 
                              {'form': form, 'trainer' : trainer, 'errors' : errors,
                               'programs' : programs}, 
                              RequestContext(request))

    else:
        form = BlitzSetupForm(None, trainer=trainer)

    return render_to_response('blitz_setup.html', 
                              {'form': form, 'trainer' : trainer, 'programs' : programs}, 
                              RequestContext(request))


@login_required
def client_setup(request, pk):
    trainer = request.user.trainer

    blitz = get_object_or_404(Blitz, pk=int(pk) )

    mode = "free" if 'free' in request.GET else None
    workoutplans = WorkoutPlan.objects.filter(trainer=trainer)

    if request.method == 'POST':
        form = NewClientForm(request.POST)
        invite = request.POST.get('invite')
        signup_key = request.POST.get('signup_key')
        invite_url = request.POST.get('invite_url')

#        import pdb; pdb.set_trace()

        if form.is_valid():

            invitation = BlitzInvitation.objects.create(
                blitz_id =  blitz.id, email = form.cleaned_data['email'], 
                name = form.cleaned_data['name'], signup_key = signup_key)

            invitation.free = True if mode == "free" else False

            # override Blitz price and workoutplan if invitation specifies either
            if 'price' in form.cleaned_data and form.cleaned_data['price']:
                invitation.price = form.cleaned_data['price']
                invitation.save()

            if 'workoutplan_id' in form.cleaned_data and form.cleaned_data['workoutplan_id']:
                workoutplan = get_object_or_404(WorkoutPlan, id=form.cleaned_data['workoutplan_id'] )
                invitation.workout_plan = workoutplan
                invitation.save()
    
            client_invite(trainer, form.cleaned_data['email'], invite_url)

            return redirect('home')
        else:
            return render_to_response('client_setup.html', 
                              {'invite' : invite, 'form': form, 'trainer' : trainer, 'blitz' : blitz,
                               'mode' : mode, 'signup_key' : signup_key, 'workoutplans' : workoutplans,
                               'invite_url' : invite_url, 'errors' : form.errors}, 
                              RequestContext(request))
    else:
        form = NewClientForm()
        signup_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))    

        uri = domain(request)

        if mode == 'free':
            invite = "Hey,\n\nI've setup your program and we're ready to start on %s. This is a one-time *FREE* pass just for you! \n Just go to the following link to sign up: %s?signup_key=%s\n\nLooking forward to tracking your progress and helping you get awesome results!\n\n%s" % (blitz.begin_date.strftime('%B %d, %Y'), uri+'/client-signup', signup_key, trainer.name)
            invite_url = uri+'/client-signup?signup_key='+signup_key
        else:
            invite = "Hey,\n\nI've setup your program and we're ready to start on %s. Just go to the following link to sign up: %s?signup_key=%s\n\nLooking forward to tracking your progress and helping you get awesome results!\n\n%s" % (blitz.begin_date.strftime('%B %d, %Y'), uri+'/client-signup', signup_key, trainer.name)
            invite_url = uri+'/'+trainer.short_name+'/'+blitz.url_slug

        return render_to_response('client_setup.html', 
                              {'invite' : invite, 'form': form, 'trainer' : trainer, 'mode' : mode,
                                'signup_key' : signup_key, 'invite_url' : invite_url, 'blitz' : blitz,
                                'errors' : form.errors, 'workoutplans' : workoutplans}, 
                              RequestContext(request))


@login_required
def spotter_program_edit(request, pk):

    trainer = request.user.trainer
    workoutplan = get_object_or_404(WorkoutPlan, pk=int(pk) )
    if len(trainer.blitz_set.all()) == 1 or not trainer.currently_viewing_blitz:
        blitz = trainer.blitz_set.all()[0]
    else:                                   
        blitz = trainer.currently_viewing_blitz

    if request.method == 'POST':
        form = SpotterProgramEditForm(request.POST)

        if form.is_valid():
            email_spotter_program_edit(pk, form.cleaned_data['edit_request'])

            return redirect('my_blitz_program')
        else:
            return render_to_response('spotter_program_edit.html', 
                              {'trainer' : trainer, 'workoutplan' : workoutplan, 'errors' : form.errors}, 
                              RequestContext(request))
    else:
        form = SpotterProgramEditForm()

        return render_to_response('spotter_program_edit.html', 
                              {'trainer' : trainer, 'workoutplan' : workoutplan, 'errors' : form.errors}, 
                              RequestContext(request))


@login_required
def upload_page(request):
    trainer = request.user.trainer

# deal with new trainer with pending documents
    numdocs = get_pending_documents('/documents', trainer.pk)

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            save_file(request.FILES['document'], trainer.pk)
            return render_to_response('upload_done_page.html', 
                              {'docs' : numdocs, 'form': form, 'trainer' : trainer}, 
                              RequestContext(request))
        else:
            return render_to_response('upload_page.html', 
                              {'docs' : numdocs, 'form': form, 'trainer' : trainer}, 
                              RequestContext(request))
    else:
        form = UploadForm()

    return render_to_response('upload_page.html', 
                              {'docs' : numdocs, 'form': form, 'trainer' : trainer}, 
                              RequestContext(request))


def save_file(file, pk_value=0, path='/documents/'):
    filename = file._get_name()

    now = datetime.datetime.now()
    output_file = "%d__%02d%02d%02d%02d%02d%02d" % (pk_value, now.year, now.month, now.day, now.hour, now.minute, now.second)
    fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + output_file), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()


@login_required
def trainer_alerts_page(request):
    trainer = request.user.trainer
    return render(request, 'trainer_alert_page.html', {
        'trainer': trainer,
        'alerts': trainer.get_alerts(),
    })

@login_required
def client_home(request, **kwargs):

    client = request.user.client

    next_workout_date = next_workout = next_workout_today = None
    if client.get_blitz().workout_plan:   # handle client on a provisional blitz (no workout_plan)
        next_workout_date, next_workout = client.get_next_workout() 
        next_workout_today = next_workout_date == client.current_datetime().date()

    show_intro = request.GET.get('show-intro') == 'true'
    if request.session.get('show_intro') is True:
        request.session.pop('show_intro')
        show_intro = True
#    if kwargs.get('show_intro') is True:
#        show_intro = True
#    if not client.has_completed_intro:
#        show_intro = True
    if request.session.get('shown_intro') is True:
        request.session.pop('shown_intro')

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            new_content.create_new_parent_comment(request.user, 
                      form.cleaned_data['comment'], 
                      timezone_now(),
                      form.cleaned_data['picture'])
        else:
            form = CommentForm()

# figure out if check-in time
    days_since_checkin = 0
    days_since_blitz = 0
    if client.checkin_set.all():
        days_since_checkin = client.checkin_set.all()[0].days_since_checkin()
    elif client.get_blitz().workout_plan:
        days_since_blitz = client.get_blitz().days_since_begin()

    return render(request, 'client_home.html', {
        'client': client,
        'next_workout': next_workout,
        'next_workout_date': next_workout_date,
        'next_workout_today': next_workout_today,
        'show_intro': show_intro,
        'shown_intro': show_intro,
        'days_since_checkin' : days_since_checkin,
        'days_since_blitz' : days_since_blitz,
        'missed_workouts': client.get_missed_workouts(),
        }, context_instance=RequestContext(request))

@login_required
def first_take(request):

    return client_home(request, show_intro=True)

@login_required()
def my_profile(request):
    if request.user.is_trainer:
        pass
    else:
        return my_client_profile(request)

@login_required
def my_client_profile(request):

    client = request.user.client
    return client_profile_history(request, client.pk)


@login_required
def client_profile(request, pk):
    return client_profile_history(request, pk)

@login_required()
def client_profile_progress(request, pk):

    client = get_object_or_404(Client, pk=int(pk) )
    gym_sessions = GymSession.objects.filter(client=client).order_by('-date_of_session')
    session_list = [ (gym_session, grouped_sets_with_user_data(gym_session)) for gym_session in gym_sessions ]

    context = {
        'client': client,
        'session_list': session_list,
        'section': 'progress',
        'lift_history_maxes': get_lift_history_maxes(client),
    }

    return render(request, 'client_profile.html', context)

@login_required()
def client_profile_checkins(request, pk):

    client = get_object_or_404(Client, pk=int(pk) )
    checkins = CheckIn.objects.filter(client=client).order_by('-date_created')
    context = {
        'client': client,
        'checkins': checkins,
        'section': 'checkins',
    }

    return render(request, 'client_profile_checkins.html', context)

@login_required()
def client_profile_history(request, pk):

    client = get_object_or_404(Client, pk=int(pk) )

    if request.user.is_trainer:
        client.units = "I" # assume Imperial units for trainers (until they have unit settings)
    else:
        client.units = request.user.client.units  # override units with viewer units

    gym_sessions = GymSession.objects.filter(client=client).order_by('-date_of_session')
    session_list = [ (gym_session, grouped_sets_with_user_data(gym_session)) for gym_session in gym_sessions if gym_session.is_logged ]

    context = {
        'client': client,
        'session_list': session_list,
        'section': 'history',
    }

    if client.get_blitz().uses_macros:
        context['macro_history'] = macro_utils.get_full_macro_history(client)

    return render( request, 'client_profile_history.html', context )

@login_required()
def client_profile_notes(request, pk):

    client = get_object_or_404(Client, pk=int(pk) )
    gym_sessions = GymSession.objects.filter(client=client).order_by('-date_of_session')
    session_list = [ (gym_session, grouped_sets_with_user_data(gym_session)) for gym_session in gym_sessions ]

    return render(request, 'client_profile_notes.html', {
        'client': client,
        'session_list': session_list,
        })

@login_required
def my_salespages(request):
    if request.user.is_trainer:
        trainer = request.user.trainer
        salespages = SalesPageContent.objects.filter(trainer=trainer)
        # sales pages for trainer's Blitzes that are either provisional or not recurring
        blitzes = Blitz.objects.filter(Q(trainer=trainer) & (Q(provisional=True) | Q(recurring=False)))
        return render(request, 'trainer_salespages.html', {
            'salespages': salespages, 'trainer': trainer, 'blitzes': blitzes,
            'SITE_URL' : domain(request) })

@login_required
def my_programs(request):
    request_blitz = request.user.blitz
    blitz = get_object_or_404(Blitz, pk=int(request_blitz.pk) )
    if request.user.is_trainer:
        workoutplans = WorkoutPlan.objects.filter(trainer = request.user.trainer)
        return render(request, 'trainer_programs.html', 
           {'trainer': request.user.trainer, 'workoutplans' : workoutplans })
    else:
        return render(request, 'blitz_program.html', {
            'blitz': blitz, 'client': request.user.client })

@login_required
def view_program(request, pk):
    workoutplan = get_object_or_404(WorkoutPlan, pk=int(pk) )
    return render(request, 'trainer_view_program.html', 
       {'workout_plan': workoutplan })

@login_required
def my_blitz_program(request):
    blitz = request.user.blitz
    return blitz_program(request, blitz.pk)

@login_required
def blitz_program(request, pk):
    blitz = get_object_or_404(Blitz, pk=int(pk) )

    if request.user.is_trainer:
        return render(request, 'blitz_program.html', {
            'blitz': blitz, 'trainer': request.user.trainer, 'SITE_URL' : settings.SITE_URL })
    else:
        return render(request, 'blitz_program.html', {
            'blitz': blitz, 'client': request.user.client, 'SITE_URL' : settings.SITE_URL })

@login_required
def my_blitz_members(request):
    blitz = request.user.blitz
    return blitz_members(request, blitz.pk)

@login_required
def blitz_members(request, pk):
    blitz = get_object_or_404(Blitz, pk=int(pk) )
    return render(request, 'blitz_members.html', {
        'blitz': blitz,
    })

@login_required()
def trainer_profile(request, pk):

    pass

def validate_set_from_post(postdata, workout_set):
    """
    Make sure POST can create a valid workout_set
    Returns True, attr_dict or False, error
    attr_dict['has_data'] indicates whether there is data for this workout_set - ie. if user left it blank
    This is *not* considered an error
    UX is probably inconsistent but the code works :)
    """

    error = None

    if 'set-%d-reps' % workout_set.pk not in postdata:
        return False, {'has_data': False}

    if not workout_set.lift.weight_or_body:
        if 'set-%d-weight' % workout_set.pk not in postdata:
            return False, {'has_data': False}

    item = {
        'has_data': True,
    }

    reps_str = postdata['set-%d-reps' % workout_set.pk]
    try:
        int(reps_str)
    except ValueError:
        return True, "Reps must be an integer"
    reps = int(reps_str)
    if reps < 0:
        return True, "Number of reps can't be negative"
    item['num_reps_completed'] = reps

    # set type if necessary
    if workout_set.lift.lift_type == 'R' and workout_set.lift.weight_or_body and workout_set.lift.allow_weight_or_body:
        item['set_type'] = postdata['%s-settype' % workout_set.lift.slug]

    # weight if necessary
    if workout_set.lift.lift_type == 'R' and (
            not workout_set.lift.weight_or_body or
            workout_set.lift.weight_or_body and workout_set.lift.allow_weight_or_body and item['set_type'] != 'B'
    ):
        weight_str = postdata['set-%d-weight' % workout_set.pk]
        if not weight_str:
            weight_str = '0'
#            return True, "Weight is required"
        try:
            float(weight_str)
        except ValueError:
            return True, "Weight must be a number"
        weight = float(weight_str)
        if weight < 0:
            return True, "Weight can't be negative"
        item['weight_in_lbs'] = weight

    return False, item

def save_set_to_session(gym_session, workout_set, item):
    """

    """
    if item['has_data'] is False:
        CompletedSet.objects.filter(gym_session=gym_session,
        workout_set=workout_set).delete()
        return

    if CompletedSet.objects.filter(gym_session=gym_session,
        workout_set=workout_set).exists():
        completed_set = CompletedSet.objects.get(gym_session=gym_session,
            workout_set=workout_set)
    else:
        completed_set = CompletedSet(gym_session=gym_session,
            workout_set=workout_set)
    completed_set.num_reps_completed = item['num_reps_completed']
    if 'weight_in_lbs' in item:
        completed_set.weight_in_lbs = item['weight_in_lbs']
    if 'set_type' in item:
        completed_set.set_type = item['set_type']
    completed_set.save()
    return completed_set

@login_required
def log_workout(request, week_number, day_char):

    error = None

    client = request.user.client
    blitz = client.get_blitz()
    plan_day = blitz.get_workout_for_day(int(week_number), day_char)
    if plan_day is None:
        raise Http404

    # assume for now that workout was done on assigned day
    gym_session = GymSession.objects.get_or_create(
        date_of_session=blitz.get_workout_date(int(week_number), day_char),
        workout_plan_day=plan_day,
        client=client
    )[0]

    grouped_sets = workout_utils.get_grouped_sets(plan_day.workout, request.user.client)
    for group in grouped_sets:
        group['set_infos'] = []
        for workout_set in group['sets']:
            set_info = {}
            set_info['workout_set'] = workout_set
            set_info['completed_set'] = None
            if CompletedSet.objects.filter(gym_session=gym_session, workout_set=workout_set).exists():
                set_info['completed_set'] = CompletedSet.objects.get(gym_session=gym_session, workout_set=workout_set)
            group['set_infos'].append(set_info)
        group['lift_summary'] = client.lift_summary(group['lift'])

    if request.method == "POST":

        has_error = False

        for group in grouped_sets:
            for set_info in group['set_infos']:
                workout_set = set_info['workout_set']
                if request.POST.get('set-%d-reps' % workout_set.pk):
                    is_error, item = validate_set_from_post(request.POST, workout_set)
                    if is_error:
                        set_info['error'] = item
                        has_error = True
                    else:
                        completed_set = save_set_to_session(gym_session, workout_set, item)
                        set_info['completed_set'] = completed_set

        if request.POST.get('notes'):
            gym_session.notes = request.POST['notes']
            gym_session.save()

        # if no errors, feed item and go home
        if not has_error:
            if not gym_session.is_logged:
                new_content.finalize_gym_session( blitz, gym_session, timezone_now() )
            return redirect('home')
        else:
            for group in grouped_sets:
                print [set_info.get('error') for set_info in group['set_infos']]

    return render(request, 'log_workout.html', {
        'client': client,
        'plan_day': plan_day,
        'workout': plan_day.workout,
        'grouped_sets': grouped_sets,
        'gym_session': gym_session,
    })

@login_required
@csrf_exempt
def save_sets(request):

    # TODO: formatting errors all raise 500 errors
    # need to refactor out of view logic and add better error handling

    if request.method != 'POST':
        raise Exception("error 29835 - must be POST")

    for key in ['sets', 'week_number', 'day_char']:
        if key not in request.POST:
            raise Exception("%s is requred" % key)

    week_number = int(request.POST['week_number'])
    day_char = request.POST['day_char']
    set_pks = [int(s) for s in request.POST['sets'].split(',')]

    client = request.user.client
    blitz = client.get_blitz()
    plan_day = blitz.get_workout_for_day(week_number, day_char)
    if plan_day is None:
        raise Exception('Invalid blitz day')

    # assume for now that workout was done on assigned day
    gym_session = GymSession.objects.get_or_create(
        date_of_session=blitz.get_workout_date(int(week_number), day_char),
        workout_plan_day=plan_day,
        client=client
    )[0]

    has_error = False
    set_errors = { pk: "" for pk in set_pks } # map of pk -> error
    for pk in set_pks:
        workout_set = WorkoutSet.objects.get(pk=pk)
        is_error, item = validate_set_from_post(request.POST, workout_set)
        if is_error:
            set_errors[pk] = item
            has_error = True
        else:
            save_set_to_session(gym_session, workout_set, item)

    # save notes when we save sets
    gym_session.notes = request.POST.get('notes', '')

    return JSONResponse({
        'has_error': has_error,
        'set_errors': set_errors
    })


@login_required
@csrf_exempt
def blitz_feed(request):
    offset = int(request.GET.get('offset', 0))
    feed_scope = (request.GET.get('feed_scope') if request.GET.get('feed_scope') else 'all')
    search_text = request.GET.get('search_text')
    feed_items = []

    try:
        obj_id = int( request.GET.get('object_id') )
    except Exception as e:
#        print e
        obj_id = None

    if search_text and len(search_text) > 0:
        clients = request.user.trainer._all_clients().filter(name__icontains=search_text)
        # blitzs = request.user.trainer.active_blitzs().filter(title__icontains=search_text)

        feed_items = FeedItem.objects.get_empty_query_set()

        # Adds client related feeds
        for client in clients:
            feed_items |= client.get_feeditems()

        # Adds client related feeds
        # for blitz in blitzs:
        #     feed_items |= blitz.get_feeditems()

        feed_items = feed_items.order_by('-pub_date')[offset:offset+10]
    else:
        if feed_scope == 'all':
            feed_items = FeedItem.objects.filter(blitz=request.user.blitz).order_by('-pub_date')[offset:offset+10]

        elif feed_scope == 'blitz':
            feed_items = FeedItem.objects.filter(blitz_id=obj_id).order_by('-pub_date')[offset:offset+10]

        elif feed_scope == 'client':
            client = Client.objects.get(pk=obj_id)
            feed_items = client.get_feeditems().order_by('-pub_date')[offset:offset+10]

    ret = {
        'feeditems': [],
        'offset': offset+10,
    }

    for feed_item in feed_items:
        ret['feeditems'].append({
            'date': feed_item.pub_date.isoformat(),
            'html': get_feeditem_html(feed_item, request.user),
        })

    return JSONResponse(ret)

def search_client_blitz(request, keyword):
    pass


def client_summary(request, pk):
    client = get_object_or_404(Client, pk=int(pk) )
    try:
        macro_goals = json.loads(client.macro_target_json)
    except Exception as e:
        print e
        macro_goals = {}
    macro_history = macro_utils.get_full_macro_history(client)

    res = {
        # 'session_list': session_list
        'client_id': {
            'id': client.pk,
            'name': client.name,
            'age': client.age,
            'weight_in_lbs': client.weight_in_lbs,
            'height_feet': client.height_feet,
            'height_inches': client.height_inches,
            'headshot': MEDIA_URL + str(client.headshot),
            'macro_target_json': client.macro_target_json
        },
        'macro_history':  macro_utils.get_full_macro_history(client),
        'html': get_client_summary_html(client, macro_goals, macro_history)
    }

    return JSONResponse(res)


@login_required
@csrf_exempt
def comment_like(request):

    comment = Comment.objects.get(pk=int(request.POST['comment_pk']))
    if comment.liked_by_user(request.user):
        return JSONResponse({'is_error': True, 'error': 'User already likes this'})

    new_content.add_like_to_comment(comment, request.user, datetime.datetime.now())

    if comment.parent_comment:
        parent = comment.parent_comment
    elif comment.gym_session:
        parent = comment.gym_session
    else:
        parent = comment

    content_type = ContentType.objects.get_for_model(parent)
    feed_item = FeedItem.objects.get(content_type=content_type, object_id=parent.pk)

    ret = {
        'is_error': False,
        'html': get_feeditem_html(feed_item, request.user)
    }

    return JSONResponse(ret)

@login_required
@csrf_exempt
def comment_unlike(request):

    comment = Comment.objects.get(pk=int(request.POST['comment_pk']))
    comment_like = CommentLike.objects.get(user=request.user, comment=comment)

    comment_like.delete()

    if comment.parent_comment:
        parent = comment.parent_comment
    elif comment.gym_session:
        parent = comment.gym_session
    else:
        parent = comment

    content_type = ContentType.objects.get_for_model(parent)
    feed_item = FeedItem.objects.get(content_type=content_type, object_id=parent.pk)

    ret = {
        'is_error': False,
        'html': get_feeditem_html(feed_item, request.user)
    }

    return JSONResponse(ret)

@login_required
@csrf_exempt
def new_comment(request):

    comment, feeditem = new_content.create_new_parent_comment(request.user, request.POST.get('comment_text'), timezone_now(), request.POST.get('comment_picture'))

    ret = {
        'is_error': False,
        'comment_html': get_feeditem_html(feeditem, request.user)
    }

    return JSONResponse(ret)

# TODO: should we abstract to a single like view?
@login_required
@csrf_exempt
def gym_session_like(request):

    gym_session = GymSession.objects.get(pk=int(request.POST['gym_session_pk']))

    new_content.add_like_to_gym_session(gym_session, request.user, datetime.datetime.now())

    content_type = ContentType.objects.get_for_model(gym_session)
    feed_item = FeedItem.objects.get(content_type=content_type, object_id=gym_session.pk)

    ret = {
        'is_error': False,
        'html': get_feeditem_html(feed_item, request.user)
    }

    return JSONResponse(ret)

@login_required
@csrf_exempt
def gym_session_unlike(request):

    gym_session = GymSession.objects.get(pk=int(request.POST['gym_session_pk']))
    gym_session_like = GymSessionLike.objects.get(user=request.user, gym_session=gym_session)
    gym_session_like.delete()

    content_type = ContentType.objects.get_for_model(gym_session)
    feed_item = FeedItem.objects.get(content_type=content_type, object_id=gym_session.pk)

    ret = {
        'is_error': False,
        'html': get_feeditem_html(feed_item, request.user)
    }
    return JSONResponse(ret)

def trainer_signup(request):

    if request.method == "POST":

        form = NewTrainerForm(request.POST)
        if form.is_valid():
            # utils.create_trainer creates Trainer and corresponding User
            trainer = utils.create_trainer(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form.cleaned_data['password1'],
                form.cleaned_data['timezone'],
                form.cleaned_data['short_name']
            )
            # create initial SalesPageContent for initial Blitz
            if trainer.name[-1] != 's':
                name = trainer.name+"'s"
            else:
                name = trainer.name+"'"

            content = create_salespagecontent("%s Page" % name, trainer)

            # create initial 1:1 (recurring, provisional) Blitz for the new Trainer
            blitz = Blitz.objects.create(trainer = trainer,
                          title = "%s Blitz" % name, recurring = True, provisional = True,
                          begin_date = trainer.current_datetime())
            blitz.sales_page_content = content
            blitz.url_slug = trainer.short_name
            blitz.price = 0
            blitz.save()


            u = authenticate(username=trainer.user.username, password=form.cleaned_data['password1'])
            login(request, u)
            request.session['show_intro'] = True
            return redirect('home')

    else:
        form = NewTrainerForm()

    args = {'default_timezone': settings.TIME_ZONE,
            'timezones': pytz.common_timezones,
            'errors' : form.errors,
            'form' : form,
           }

    return render(request, 'trainer_register.html', args)


def client_signup(request):

    invitation = get_object_or_404(BlitzInvitation, signup_key=request.GET.get('signup_key'))

    if not invitation.free:
        blitz = get_object_or_404(Blitz, id=invitation.blitz_id)
        return redirect("/%s/%s/signup?signup_key=%s" % (blitz.trainer.short_name, blitz.url_slug, request.GET.get('signup_key')))

    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            client = utils.create_client(
                invitation.name,
                invitation.email,
                form.cleaned_data['password1']
            )
            utils.add_client_to_blitz(invitation.blitz, client, invitation.workout_plan)
            alert = TrainerAlert.objects.create(
                       trainer=invitation.blitz.trainer, text="New client registration.",
                       client_id=client.id, alert_type = 'X', date_created=time.strftime("%Y-%m-%d"))

            u = authenticate(username=client.user.username, password=form.cleaned_data['password1'])
            login(request, u)
            request.session['show_intro'] = True
            return redirect('home')

    else:
        form = SetPasswordForm()

    return render(request, 'client_signup.html', {
        'invitation': invitation,
        'form': form,
    })

@login_required
@csrf_exempt
def set_intro_1(request):

    client = request.user.client

    form = Intro1Form(request.POST)
    if form.is_valid():
        client.age = form.cleaned_data['age']
        client.weight_in_lbs = form.cleaned_data['weight']
        client.height_feet = form.cleaned_data['height_feet']
        client.height_inches = form.cleaned_data['height_inches']
        client.gender = form.cleaned_data['gender']
        client.save()
        ret = {
            'is_error': False,
        }
    else:
        ret = {
            'is_error': True,
            'errors': form.errors,
        }

    return JSONResponse(ret)

@login_required
@csrf_exempt
def new_child_comment(request):

    # todo: authx - user in a diff blitz could add a comment

    if request.POST.get('content_type') == 'comment':
        comment = Comment.objects.get(pk=int(request.POST['object_pk']))
        new_content.add_child_to_comment(comment, request.user, request.POST['comment_text'], timezone_now())
        content_type = ContentType.objects.get_for_model(comment)
        feed_item = FeedItem.objects.get(content_type=content_type, object_id=comment.pk)

    elif request.POST.get('content_type') == 'gym session':
        gym_session = GymSession.objects.get(pk=int(request.POST['object_pk']))
        new_content.add_comment_to_gym_session(gym_session, request.user, request.POST['comment_text'], timezone_now())
        content_type = ContentType.objects.get_for_model(gym_session)
        feed_item = FeedItem.objects.get(content_type=content_type, object_id=gym_session.pk)

    ret = {
        'is_error': False,
        'html': get_feeditem_html(feed_item, request.user)
    }

    return JSONResponse(ret)

# No login required for sales pages
# /{slug} sales page (initial blitz url_slug is same as trainer short_name)
def default_blitz_page(request, short_name):
    return blitz_page(request, short_name, short_name)

def blitz_page(request, short_name, url_slug):

    trainer = Trainer.objects.filter(short_name__iexact=short_name)
    blitz = sales_page = None
    if trainer:
        if trainer[0].blitz_set.filter(url_slug__iexact=url_slug):
            blitz = trainer[0].blitz_set.filter(url_slug__iexact=url_slug)[0]
            sales_page = blitz.sales_page_content
        else:
            blitz = None
            sales_page = None

    if sales_page and trainer:
        return render(request, "sales_blitz.html", {
            'blitz' : blitz, 'trainer' : trainer[0], 'sales_page': sales_page })
    else:
        return redirect('home')

# No login required for sales pages
def sales_blitz(request):

    debug_mode = False
    debug_key = None
    if 'debug' in request.GET:
        debug_mode = request.GET.get('debug')
    if 'key' in request.GET:
        debug_key = request.GET.get('key')
    if 'slug' in request.GET:
        trainer = get_object_or_404(Trainer, short_name=request.GET.get('short_name'))
        blitz = get_object_or_404(Blitz, trainer=trainer, url_slug=request.GET.get('slug'))
        if blitz.sales_page_content.sales_page_key != debug_key:
            debug_mode = False
        sales_page = blitz.sales_page_content
    else:
        blitz = None

    if blitz and request.method == 'POST':
        if 'intro' in request.POST:
            blitz.sales_page_content.program_introduction = request.POST.get('intro')

        if 'datepicker' in request.POST:
            try:
                # set date, keeping in mind model will force begin to Monday
                blitz.begin_date = datetime.datetime.strptime(request.POST.get('datepicker'), '%Y-%m-%d').date()
            except:
                pass

#        import pdb; pdb.set_trace()
        
        if 'price' in request.POST:
            if request.POST.get('price').isdigit():
                blitz.price = request.POST.get('price')
        if 'price_model' in request.POST:
            blitz.price_model = request.POST.get('price_model')
        if 'why' in request.POST:
            blitz.sales_page_content.program_why = request.POST.get('why')
        if 'who' in request.POST:
            blitz.sales_page_content.program_who = request.POST.get('who')
        if 'last' in request.POST:
            blitz.sales_page_content.program_last_words = request.POST.get('last')

        form = SalesBlitzForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            if form.cleaned_data['logo_picture']:
                blitz.sales_page_content.logo = form.cleaned_data['logo_picture']
            if form.cleaned_data['picture']:
                blitz.sales_page_content.trainer_headshot = form.cleaned_data['picture']

        blitz.sales_page_content.save()
        blitz.save()

    return render(request, "sales_blitz.html", {
        'blitz' : blitz, 'trainer' : blitz.trainer, 'sales_page': sales_page, 'debug_mode' : debug_mode
    })

def sales_page(request, plan_slug):

    blitz = get_object_or_404(Blitz, url_slug=plan_slug)
    template = 'sales_pages/%s.html' % plan_slug.lower()

    return render(request, template, {
        'blitz': blitz,
    })

def sales_page_2(request, urlkey):

    blitz = get_object_or_404(Blitz, urlkey=urlkey)
    template = 'sales_page.html'

    return render(request, template, {
        'blitz': blitz,
        'sales_content': blitz.sales_page_content,
    })

def default_blitz_signup(request, short_name):
    return blitz_signup(request, short_name, short_name)

def blitz_signup(request, short_name, url_slug):

    if 'signup_key' in request.GET:
        invitation = get_object_or_404(BlitzInvitation, signup_key=request.GET.get('signup_key'))
    else:
        invitation = None

    trainer = get_object_or_404(Trainer, short_name=short_name)
    blitz = get_object_or_404(Blitz, trainer=trainer, url_slug=url_slug)
    next_url = '/signup-complete?pk='+str(blitz.pk)

    return render(request, 'blitz_signup.html', {
        'blitz': blitz, 'trainer': trainer, 'invitation': invitation,
        'marketplace_uri': settings.BALANCED_MARKETPLACE_URI,
        'next_url': next_url,
    })

def blitz_signup_done(request):

    blitz = get_object_or_404(Blitz, pk=request.GET.get('pk'))

    return render(request, 'blitz_signup_done.html', {
        'blitz': blitz,
    })

@csrf_exempt
def create_account_hook(request, pk):

    # TODO: there is a race condition if someone else (ie same user in another tab)
    # signs up with the same email address before card is processed. whatever.

    blitz = get_object_or_404(Blitz, pk=pk)
    form = CreateAccountForm(request.POST)
    if form.is_valid():
        request.session['name'] = form.cleaned_data['name']
        request.session['email'] = form.cleaned_data['email']
        request.session['password'] = form.cleaned_data['password']
        has_error = False
        errors = {}
    else:
        has_error = True
        errors = dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()])

    ret = {
        'has_error': has_error,
        'errors': errors,
    }

    return JSONResponse(ret)

@csrf_exempt
def payment_hook(request, pk):

    blitz = get_object_or_404(Blitz, pk=pk)
    form = SubmitPaymentForm(request.POST)
    has_error = False
    error = ""
    if form.is_valid():

        # process payment w/balanced 1.1 API
        import balanced

#        import pdb; pdb.set_trace()    

        if 'invitation' in request.GET:
            invitation = get_object_or_404(BlitzInvitation, pk=request.GET.get('invitation'))
        else:
            invitation = None
        
        marketplace = balanced.Marketplace.query.one()
        try:
            card = balanced.Card.fetch(form.cleaned_data['card_uri'])
            # charge card
            if invitation:
                debit_amount_str = "%d00" % invitation.price
            else:
                debit_amount_str = "%d00" % blitz.price

            card.debit(appears_on_statement_as = 'Blitz.us payment',
                       amount = debit_amount_str,
                       description='Blitz.us payment')
        except:
            has_error = True
            error = "Card could not be charged. Please try another card. "
            # Update ChargeSetting, Payment records

        if not error:
            client = utils.get_or_create_client(
                request.session['name'],
                request.session['email'].lower(),
                request.session['password']
            )
            client.balanced_account_uri = card.href
            client.save()

            # Update ChargeSetting, Payment records

            if invitation:
                utils.add_client_to_blitz(blitz, client, invitation.workout_plan, invitation.price)
            else:
                utils.add_client_to_blitz(blitz, client)

            emails.signup_confirmation(client)

            mail_admins('we got a signup bitches!', '%s signed up for %s' % (str(client), str(blitz)))

            user = authenticate(username=client.user.username, password=request.session['password'])
            login(request, user)
            request.session['show_intro'] = True
            if 'name' in request.session:
                request.session.pop('name')
            if 'email' in request.session:
                request.session.pop('email')
            if 'password' in request.session:
                request.session.pop('password')

    else:
        has_error = True
        error = "Invalid card data"

    ret = {
        'has_error': has_error,
        'error': error,
    }
    return JSONResponse(ret)


@login_required
@csrf_exempt
def trainer_dismiss_alert(request):

    trainer = request.user.trainer
    alert_pk = int(request.POST['alert_pk'])
    alert = TrainerAlert.objects.get(pk=alert_pk)
    alert.trainer_dismissed = True
    alert.save()

    return JSONResponse({'is_error': False})

@login_required
def set_up_profile_basic(request):
    client = request.user.client


    if request.method == 'POST':
        form = Intro1Form(request.POST)
        if form.is_valid():
            client.age = form.cleaned_data['age']

            if form.cleaned_data['units'] == "M":
                client.units = 'M'
                client.weight_in_lbs = float(units_tags.kg_conversion(form.cleaned_data['weight'], client))
                inches = float(float(units_tags.m_conversion(form.cleaned_data['height_feet'], client)) 
                             + float(units_tags.cm_conversion(form.cleaned_data['height_inches'], client)))
                client.height_feet, client.height_inches = divmod(inches,12)

            else:
                client.units = 'I'
                client.weight_in_lbs = form.cleaned_data['weight']
                client.height_feet = form.cleaned_data['height_feet']
                client.height_inches = form.cleaned_data['height_inches']
            
            client.gender = form.cleaned_data['gender']

            client.save()

            request.session['intro_stage'] = 'photo'
            return redirect('set_up_profile')

    else:
        form = Intro1Form()

    return render(request, 'signup/basic.html', {
        'client': client,
        'form': form,
    })


    if request.method == 'POST':
        form = ClientSettingsForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            
            client.headshot = form.cleaned_data['picture']
            client.save()
            client.headshot_from_image(settings.MEDIA_ROOT+'/'+client.headshot.name)


@login_required
def set_up_profile_photo(request):
    client = request.user.client
    if request.method == 'POST':
        form = ProfileURLForm(request.POST, request.FILES)
    
#        import pdb; pdb.set_trace()
        if form.is_valid() and form.is_multipart():
            client.headshot = form.cleaned_data['picture']
            client.save()
            client.headshot_from_image(settings.MEDIA_ROOT+'/'+client.headshot.name)

            client.has_completed_intro = True
            client.save()

        request.session['intro_stage'] = 'summary'
        return redirect('set_up_profile')

    else:
        form = ProfileURLForm()

    return render(request, 'signup/photo.html', {
        'client': client,
        'form': form,
    })

@login_required
def set_up_profile_summary(request):

    client = request.user.client

    return render(request, 'signup/summary.html', {
        'client': client,
    })

@login_required
def set_up_profile(request):

    intro_stage = request.session.get('intro_stage', 'basic')

    if intro_stage == 'basic':
        return set_up_profile_basic(request)

    elif intro_stage == 'photo':
        return set_up_profile_photo(request)

    elif intro_stage == 'summary':
        return set_up_profile_summary(request)


@login_required
def client_checkin(request):
    client = request.user.client
    # get today's checkins, assume one per day max
    checkins = CheckIn.objects.filter(date_created__year=client.current_datetime().date().year,
                                      date_created__month=client.current_datetime().date().month,
                                      date_created__day=client.current_datetime().date().day)
    if checkins:
        checkin = checkins[0]
    else:
        checkin = CheckIn()

    if request.method == 'POST':
        form = ClientCheckinForm(request.POST, request.FILES)

#        import pdb; pdb.set_trace()

        if form.is_valid() and form.is_multipart():

            if form.cleaned_data['front_image']:
                checkin.front_image = form.cleaned_data['front_image']
            if form.cleaned_data['side_image']:
                checkin.side_image = form.cleaned_data['side_image']

            if form.cleaned_data['weight']:
                checkin.weight = float(units_tags.kg_conversion(form.cleaned_data['weight'], client))
            checkin.client = client
            checkin.save()

            alert = TrainerAlert.objects.create(
                       trainer=client.get_blitz().trainer, text="checked-in.",
                       client_id=client.id, alert_type = 'X', date_created=time.strftime("%Y-%m-%d"))

            if form.data['done'] == '1':
                return redirect('home')
        else:
            if form.data['done'] == '1':
                return redirect('home')
            else:
                return render(request, 'checkin.html', { 'client': client, 'checkin' : checkin })
    else:
        form = ClientCheckinForm()

    return render(request, 'checkin.html', { 'client': client, 'checkin' : checkin })

@login_required
def client_settings(request):

    client = request.user.client

    if request.method == 'POST':
        form = ClientSettingsForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            client.headshot = form.cleaned_data['picture']
            client.save()
            client.headshot_from_image(settings.MEDIA_ROOT+'/'+client.headshot.name)

        else:
            return render(request, 'client_profile_settings.html', {
                'client': client,
                'section': 'settings',
                'timezones': pytz.common_timezones,})
    else:
        form = ClientSettingsForm()

    return render(request, 'client_profile_settings.html', {
        'client': client,
        'section': 'settings',
        'timezones': pytz.common_timezones,})


def staff_login(request):

    if not request.user.is_superuser:
        return HttpResponse("Invalid")

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        user.backend='django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('home')
    else:
        form = LoginForm()

    #displays the error but preserves the e-mail address entered
    return render(request, "login.html", {
        'form': form,
    })


def set_client_macros(request, pk):

    trainer = request.user.trainer
    client = get_object_or_404(Client, pk=int(pk))

    has_error = False
    success = False

    if request.method == "POST":
        form = SetMacrosForm(request.POST)
        if form.is_valid():
            client.macro_target_json = json.dumps(form.cleaned_data)
            client.save()
            success = True
        else:
            has_error = True
    else:
        if client.macro_target_json:
            form = SetMacrosForm(client.macro_target_spec())
        else:
            form = SetMacrosForm()

    return render(request, 'set_client_macros.html', {
        'client': client,
        'form': form,
        'has_error': has_error,
        'success': success,
    })

# ERROR handling
def page404(request):
    return render(request, '404.html')

def page500(request):
    return render(request, '500.html')

def not_found_error(request, template_name='404.html'):

    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )

def server_error(request, template_name='500.html'):

    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )

def permission_denied_error(request, template_name='500.html'):

    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )

def bad_request_error(request, template_name='500.html'):

    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )

@login_required
@csrf_exempt
def set_timezone(request):

    client = request.user.client
    client.timezone = request.POST['timezone']
    client.save()
    return JSONResponse({'is_error': False})

@login_required
@csrf_exempt
def set_units(request):

    client = request.user.client
    client.units = request.POST['units']
    client.save()
    return JSONResponse({'is_error': False})


@csrf_exempt
def errorlog(request):

    # Adding a single user hack because one of our idiot clients generates a JS error on every page
    if request.POST.get('details') and '_TPIHelper' in request.POST['details'][0]:
        pass
    else:
        logger = logging.getLogger(__name__)
        logger.error('JS error', extra={'request': request})
    return HttpResponse(json.dumps({'success': True}))


@login_required
def trainer_switch_blitz(request):

    blitz_pk = request.GET.get('new_blitz')
    blitz = Blitz.objects.get(pk=blitz_pk)
    request.user.trainer.set_currently_viewing_blitz(blitz)
    return redirect('home')


@login_required
def trainer_switch_blitz_program(request):

    blitz_pk = request.GET.get('new_blitz')
    blitz = Blitz.objects.get(pk=blitz_pk)
    request.user.trainer.set_currently_viewing_blitz(blitz)
    return redirect('my_blitz_program')

# open permalink
def single_post_gym(request, pk):
    feeditem = get_object_or_404(FeedItem, pk=int(pk))
    gym_session = feeditem.content_object
    feeditem_html = get_feeditem_html(feeditem, request.user)
    return render(request, 'single_post.html', {'feeditem': feeditem, 'feeditem_html': feeditem_html})

# open permalink
def single_post_comment(request, pk):
    feeditem = get_object_or_404(FeedItem, pk=int(pk))
    feeditem_html = get_feeditem_html(feeditem, request.user)
    return render(request, 'single_post.html', {'feeditem': feeditem, 'feeditem_html': feeditem_html})

@login_required
def trainer_dashboard(request):
    user_id = request.user.pk

    blitzes = request.user.trainer.active_blitzes()
    clients = request.user.trainer.all_clients()

    heading = Heading.objects.all().order_by('?')[:1].get()
    header = "%s - %s" % (heading.saying, heading.author)

    if blitzes and clients:
        return render(request, 'trainer_dashboard.html', {'clients': clients, 'blitzes': blitzes, 'user_id': user_id, 'macro_history':  macro_utils.get_full_macro_history(clients[0]), 'header': header})
    else:
        return redirect('home')


