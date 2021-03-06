from base.models import Trainer, Client, BlitzMember, BlitzInvitation, Comment, FeedItem, CompletedSet, GymSession, SalesPageContent
from base.new_content import finalize_gym_session

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from workouts import utils as workout_utils
from workouts.models import WorkoutSet, Lift, Workout, ExerciseCustom
from base.templatetags import units_tags

import hashlib
import datetime
import json
import itertools
import random
import string

MEDIA_URL = getattr(settings, 'MEDIA_URL')
STATIC_URL = getattr(settings, 'STATIC_URL')

def test_mail():
    msg = EmailMessage('Hi','Test email', to=['georgek@gmail.com'])
    msg.send()
    return True

def try_float(string, fail=None):
    try:
        return float(string)
    except Exception:
        return fail;

def get_character_for_user(user):
    """
    Return a (user_type, obj) tuple for a user
    user_type is "T" or "D"; and obj is associated model
    """

    try:
        return ('T', user.trainer)
    except ObjectDoesNotExist:
        pass

    try:
        return ('D', user.client.name)
    except:
        raise Exception("No character for user")

def create_trainer(name, email, password, timezone=None, short_name=""):
    """
    Make and save a new trainer (with user)
    """
    if timezone == None:
        timezone = getattr(settings, 'TIME_ZONE')

    username = hashlib.md5(email).hexdigest()[:20]
    user = User.objects.create_user( username=username, email=email, password=password )
    trainer = Trainer(user=user, name=name, timezone=timezone, short_name=short_name)
    trainer.save()
    return trainer

def create_client(name, email, password, age=None, weight_in_lbs=None, height_feet=None, height_inches=None, gender="U"):
    """
    Make and save client
    """
    username = hashlib.md5(email).hexdigest()[:20]
    user = User.objects.create_user( username=username, email=email, password=password )
    client = Client(user=user, name=name, age=age, weight_in_lbs=weight_in_lbs, height_feet=height_feet, height_inches=height_inches, gender=gender)
    client.save()
    return client

def get_or_create_client(name, email, password, age=None, weight_in_lbs=None, height_feet=None, height_inches=None, gender="U"):
    """
    Make and save client
    """
    if Client.objects.filter(user__email=email).exists():
        client = Client.objects.get(user__email=email)
        # todo: update fields?
        return client
    else:
        return create_client(name, email, password, age, weight_in_lbs, height_feet, height_inches, gender)

def create_salespagecontent(name, trainer, key=None, title=None):

    content = SalesPageContent.objects.create(name = name, trainer = trainer)
    content.program_introduction = "I'm taking a limited number of awesome, highly-motivated people for a new online coaching program."
    content.program_why = "I've been coaching--and coaching online--for a long time. I've seen what works and what doesn't, and know that it's not just about making a program that's effective, but one you can stick to. Mixing years of training and nutrition experience with a good dash of psychology, I think I've got something that can really help people take their fitness to the next level."
    content.program_who = "If you're familiar with basic lifts and nutrition, but need a more personalized approach and expert feedback to push yourself to the next level, I think I can help you out."
    content.program_last_words = "If you're having second thoughts, working with me might not be for you. To get the most out of working with me, I need you to be focused, motivated, and ready to put in the work to get the results you deserve. You show up with that, and I'll do the rest."
    content.program_title = title if title else "%s Program" % name
    content.sales_page_key = key if key else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    content.save()
    return content

#TODO handle macro_formula optional param
def add_client_to_blitz(blitz, client, workoutplan=None, price=0, start_date=None, macro_formula=None, invitation=None):

    # for a Provisional 1:1 (recurring) blitz, add client to a copy of the provisional instance
    if blitz.provisional:
        blitz.pk = None
        blitz.provisional = False
        blitz.recurring = True
        blitz.title = "individual:%s blitz:%s" % (client.name, blitz.url_slug)
        blitz.workout_plan = workoutplan
        blitz.price = price
        blitz.url_slug = ''
        blitz.uses_macros = True
        blitz.macro_strategy = macro_formula if macro_formula else 'DEFAULT'
        blitz.save()

    if not start_date:
        start_date = client.current_datetime().date()

    membership = BlitzMember.objects.create(blitz=blitz, client=client, date_created=start_date)
    # remove invitation if applicable and transfer price to new membership
    if invitation:
        membership.price = invitation.price
        invitation.delete()
    else:
        membership.price = price

    membership.save()

    return membership

# TODO: should be instance method of GymSession
def grouped_sets_with_user_data(gym_session):
    """
    wrapper around (workouts) get_grouped_sets - "sets" is a list of (set, completed_set) tuples
    """
#    import pdb; pdb.set_trace()

    workout = gym_session.workout_plan_day.workout
    grouped_sets = workout_utils.get_grouped_sets(workout)
    for d in grouped_sets:
        sets = []
        for set in d['sets']:
            try:
                completed_set = CompletedSet.objects.get(gym_session=gym_session, workout_set=set)
            except ObjectDoesNotExist:
                completed_set = None
            sets.append( (set, completed_set) )
        d['sets'] = sets

    return grouped_sets

def JSONResponse(content):
    return HttpResponse(json.dumps(content), mimetype="application/json")

def get_blitz_group_header_html(blitz, title, start_date, end_date, headshots):
    return render_to_string('dashboard/blitz_group_header.html', {
        'blitz': blitz,
        'title': title,
        'start_date': start_date,
        'end_date': str(blitz.end_date()),
        'headshots': headshots,
        'members_count': len(headshots)
    })

def get_feeditem_html(feed_item, user):
    if feed_item.content_type.name == 'comment':
        return render_to_string('feeditems/comment.html', {
            'comment': feed_item.content_object,
            'feed_item': feed_item,
            'user': user,
        })

    elif feed_item.content_type.name == 'gym session':
        return render_to_string('feeditems/gym_session.html', {
            'gym_session': feed_item.content_object,
            'exercises': grouped_sets_with_user_data(feed_item.content_object),
            'feed_item': feed_item,
            'user': user
        })

    elif feed_item.content_type.name == 'check in':
        return render_to_string('feeditems/checkins.html', {
            'checkin': feed_item.content_object,
            'user': user,
            'feed_item': feed_item,
            'MEDIA_URL': MEDIA_URL
        })

def get_client_summary_html(client, macro_goals, macro_history):
    macro_goals_formatted = {}
    for k in macro_goals:
        # Converts number to 'k' if the number is greater/equal than 1000 and adds 'k' sufix
        if macro_goals[k] >= 1000:
            macro_goals_formatted[k] =  '{:.1f}k'.format(macro_goals[k]/1000.00)
        else:
            macro_goals_formatted[k] =  macro_goals[k]

    customizations = ExerciseCustom.objects.filter(client=client).order_by('-pk')
    workout_info = get_workout_info(client)

    return render_to_string('dashboard/client_summary.html', {
        'client': client,
        'macro_goals': macro_goals_formatted,
        'macro_details': macro_goals,
        'macro_history': macro_history,
        'customizations': customizations,
        'workout_info': workout_info,
        'MEDIA_URL': MEDIA_URL
    })

def get_invitee_summary_html(invitation, delta, macro_goals):
    macro_goals_formatted = {}
    detailed_macros = False
    for k in macro_goals:
        # Converts number to 'k' if the number is greater/equal than 1000 and adds 'k' sufix
        if macro_goals[k] >= 1000:
            macro_goals_formatted[k] =  '{:.1f}k'.format(macro_goals[k]/1000.00)
        else:
            macro_goals_formatted[k] =  macro_goals[k]
        detailed_macros = True

    return render_to_string('dashboard/invitee_summary.html', {
        'invitation': invitation,
        'delta': delta,
        'macro_goals': macro_goals_formatted,
        'macro_details': macro_goals,
        'detailed_macros': detailed_macros,
        'STATIC_URL': STATIC_URL
    })


def get_inboxfeed_html(user_threads):
    return render_to_string('messages/inbox_inner.html', {'user_threads': user_threads})

def new_gym_session_from_file(client, file_path, week, day):
    """
    Create new gym session for client with the contents from file
    """
    blitz = client.get_blitz()
    plan_day = blitz.get_workout_for_day(week, day)
    workout = plan_day.workout
    gym_date = blitz.get_workout_date(week, day)
    gym_session = GymSession.objects.create(date_of_session=gym_date, workout_plan_day=plan_day, client=client)

    sets = []
    for line in open(file_path):
        lift_slug, reps, weight = line.strip().split('\t')
        sets.append( ( lift_slug, reps, weight) )

    exercises = itertools.groupby(sets, key=lambda x: x[0])
    for slug, v in exercises:
        workout_sets = list(WorkoutSet.objects.filter(workout=workout, lift__slug=slug))
        for i, setinfo in enumerate(v):
            CompletedSet.objects.create(
                gym_session=gym_session,
                workout_set=workout_sets[i],
                num_reps_completed=int(setinfo[1]),
                weight_in_lbs=float(setinfo[2])
            )

    finalize_gym_session(blitz, gym_session, datetime.datetime.combine(gym_session.date_of_session, datetime.time() ))

def get_lift_history(client):
    """
    For each lift, give a list of all past exercises
    Ordered from beginning
    """
    lifts = {}
    for gym_session in GymSession.objects.filter(client=client):
        for d in grouped_sets_with_user_data(gym_session):
            if d['lift'] not in lifts:
                lifts[d['lift']] = []
            lifts[d['lift']].append( (gym_session, d['sets']) )
    return lifts

def get_max_set(sets):
    m = None
    for workout_set, completed_set in sets:
        if not completed_set:
            continue
        if not m:
            m = completed_set
        if completed_set.weight_in_lbs > m.weight_in_lbs:
            m = completed_set
    return m

def get_lift_history_maxes(client):
    """
    For each lift, give a list of all past exercises
    Ordered from beginning
    """
    lifts = {}
    for lift, t in get_lift_history(client).items():
        l = []
        for gym_session, sets in t:
            m = get_max_set(sets)
            if m:
                l.append( (gym_session, m) )
        lifts[lift] = l
    return lifts

def get_workout_info(client, days=7):
    DAYS_OF_WEEK = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'H': 'Thursday', 'F': 'Friday', 'S': 'Saturday', 'U': 'Sunday'}

    missed_workouts = []

    if client.get_blitz().workout_plan:
        for n in range(days):    # default to a week
            day = client.current_datetime().date() + datetime.timedelta(days=-n)
            day_workout = client.get_blitz().get_workout_for_date(day)
            if day_workout and not client.gymsession_set.filter(workout_plan_day=day_workout).exists():
                missed_workouts.append(
                   { 'day': DAYS_OF_WEEK[day_workout.day_of_week], 
                     'lift': day_workout.workout.display_name,
                   })

    return missed_workouts

# utility method for upload_page
def save_file(file, pk_value=0, path='/documents/'):
    if pk_value != 0:
        trainer = get_object_or_404(Trainer, pk=pk_value)
    else:
        trainer = Trainer()

    filename = file._get_name()

    # get file extention
    if len(filename.split('.')) > 1:
        ext = filename.split('.')[1]
    else:
        ext = None

    now = datetime.datetime.now()
    if ext:
        output_file = "%d__%02d%02d%02d%02d%02d%02d_%s.%s" % (pk_value, now.year, now.month, now.day, now.hour, now.minute, now.second, trainer.short_name, ext)
    else:
        output_file = "%d__%02d%02d%02d%02d%02d%02d_%s" % (pk_value, now.year, now.month, now.day, now.hour, now.minute, now.second, trainer.short_name)

    fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + output_file), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return output_file

# given a macro formula, set macros for specified blitz and all or (optional) specified client
def blitz_macros_set(blitz, formula, client=None, macros_data=None):
    if client:
        clients = [client]
    else:
        clients = blitz.members()

    for client in clients:
        # for invitee we'll use sample biometrics
        age = float(30) if not client.age else float(client.age)
        kg = float(100) if not client.weight_in_lbs else float(client.weight_in_lbs * 0.45359237)
        cm = float(180) if not client.height_feet else float(units_tags.feet_conversion(client, True))
        wkout_factor = float(1.15)   # % workout day above rest day
        min_factor = float(0.8)      # % min below

        if formula == 'BULK':
            factor = float(1.1)
        elif formula == 'CUT':
            factor = float(0.9)
        elif formula == 'BEAST':
            factor = float(1.15)
        else:
            factor = float(1.0)

        if client.gender == 'F':
            r_cals = float((10 * kg + 6.25 * cm - 5 * age - 161) * factor)
        else:
            r_cals = float((10 * kg + 6.25 * cm - 5 * age + 5) * factor)

        r_protein = (0.9 * kg * 2.2) * factor
        r_fat = (0.4 * kg * 2.2) * factor
        r_carbs = (r_cals - r_protein - r_fat) / 4 * factor
        w_cals = r_cals * wkout_factor
        w_protein = r_protein * wkout_factor
        w_fat = r_fat * wkout_factor
        w_carbs = r_carbs * wkout_factor

        if macros_data:   # overwrite formula if client macros entered

            if 'c_rest_cals' in macros_data:   # called from macros forms, needs transform
                r_cals = float(macros_data['c_rest_cals']) if macros_data['c_rest_cals'].isdigit() else 0
                r_protein = float(macros_data['c_rest_protein']) if macros_data['c_rest_protein'].isdigit() else 0
                r_fat = float(macros_data['c_rest_fat']) if macros_data['c_rest_fat'].isdigit() else 0
                r_carbs = float(macros_data['c_rest_carbs']) if macros_data['c_rest_carbs'].isdigit() else 0
                w_cals = float(macros_data['c_wout_cals']) if macros_data['c_wout_cals'].isdigit() else 0
                w_protein = float(macros_data['c_wout_protein']) if macros_data['c_wout_protein'].isdigit() else 0
                w_fat = float(macros_data['c_wout_fat']) if macros_data['c_rest_cals'].isdigit() else 0
                w_carbs = float(macros_data['c_wout_carbs']) if macros_data['c_wout_carbs'].isdigit() else 0

                client.macro_target_json = '{"training_protein_min": %0.0f, "training_protein": %0.0f, "rest_protein_min": %0.0f, "rest_protein": %0.0f, "training_carbs_min": %0.0f, "training_carbs": %0.0f, "rest_carbs_min": %0.0f, "rest_carbs": %0.0f, "training_calories_min": %0.0f, "training_calories": %0.0f, "rest_calories_min": %0.0f, "rest_calories": %0.0f, "training_fat_min": %0.0f, "training_fat": %0.0f, "rest_fat_min": %0.0f, "rest_fat": %0.0f}' % ( w_protein*min_factor, w_protein, r_protein*min_factor, r_protein, w_carbs*min_factor, w_carbs, r_carbs*min_factor, r_carbs, w_cals*min_factor, w_cals, r_cals*min_factor, r_cals, w_fat*min_factor, w_fat, r_fat*min_factor, r_fat )

            elif 'rest_calories' in macros_data:  # called during on-boarding, same format
                client.macro_target_json = macros_data

        client.save()

    return

# given a macro formula, set macros for invitee
# TODO: reuse code from both _macros_set functions to avoid duplication
def invitee_macros_set(invitee, formula, macros_data=None):

    if invitee:
        age = float(30)
        kg = float(100)
        cm = float(180)
        wkout_factor = float(1.15)   # % workout day above rest day
        min_factor = float(0.8)      # % min below

        if formula == 'BULK':
            factor = float(1.1)
        elif formula == 'CUT':
            factor = float(0.9)
        elif formula == 'BEAST':
            factor = float(1.15)
        else:
            factor = float(1.0)

        r_cals = float((10 * kg + 6.25 * cm - 5 * age + 5) * factor)

        r_protein = (0.9 * kg * 2.2) * factor
        r_fat = (0.4 * kg * 2.2) * factor
        r_carbs = (r_cals - r_protein - r_fat) / 4 * factor
        w_cals = r_cals * wkout_factor
        w_protein = r_protein * wkout_factor
        w_fat = r_fat * wkout_factor
        w_carbs = r_carbs * wkout_factor

        if macros_data:   # overwrite formula if client macros entered
            if 'c_rest_cals' in macros_data:   # called from macros forms, needs transform
                r_cals = float(macros_data['c_rest_cals']) if macros_data['c_rest_cals'].isdigit() else 0
                r_protein = float(macros_data['c_rest_protein']) if macros_data['c_rest_protein'].isdigit() else 0
                r_fat = float(macros_data['c_rest_fat']) if macros_data['c_rest_fat'].isdigit() else 0
                r_carbs = float(macros_data['c_rest_carbs']) if macros_data['c_rest_carbs'].isdigit() else 0
                w_cals = float(macros_data['c_wout_cals']) if macros_data['c_wout_cals'].isdigit() else 0
                w_protein = float(macros_data['c_wout_protein']) if macros_data['c_wout_protein'].isdigit() else 0
                w_fat = float(macros_data['c_wout_fat']) if macros_data['c_rest_cals'].isdigit() else 0
                w_carbs = float(macros_data['c_wout_carbs']) if macros_data['c_wout_carbs'].isdigit() else 0

                invitee.macro_target_json = '{"training_protein_min": %0.0f, "training_protein": %0.0f, "rest_protein_min": %0.0f, "rest_protein": %0.0f, "training_carbs_min": %0.0f, "training_carbs": %0.0f, "rest_carbs_min": %0.0f, "rest_carbs": %0.0f, "training_calories_min": %0.0f, "training_calories": %0.0f, "rest_calories_min": %0.0f, "rest_calories": %0.0f, "training_fat_min": %0.0f, "training_fat": %0.0f, "rest_fat_min": %0.0f, "rest_fat": %0.0f}' % ( w_protein*min_factor, w_protein, r_protein*min_factor, r_protein, w_carbs*min_factor, w_carbs, r_carbs*min_factor, r_carbs, w_cals*min_factor, w_cals, r_cals*min_factor, r_cals, w_fat*min_factor, w_fat, r_fat*min_factor, r_fat )

            elif 'rest_calories' in macros_data:  # called during on-boarding, same format
                invitee.macro_target_json = macros_data

        invitee.save()

    return

