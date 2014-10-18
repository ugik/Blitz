from base.models import Trainer, Client, BlitzMember, Comment, FeedItem, CompletedSet, GymSession, SalesPageContent
from base.new_content import finalize_gym_session

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from workouts import utils as workout_utils
from workouts.models import WorkoutSet, Lift, Workout

import hashlib
import datetime
import json
import itertools
import random
import string

MEDIA_URL = getattr(settings, 'MEDIA_URL')

def test_mail():
    msg = EmailMessage('Hi','Test email', to=['georgek@gmail.com'])
    msg.send()
    return True

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
    content.program_introduction = "TRAINER INTRO... type here how you introduce your training program..."
    content.program_why = "WHY... type here why people should sign up for your program..."
    content.program_who = "WHO... type here who should sign up for your program..."
    content.program_last_words = "LAST WORDS... here's your chance to bring it home!"
    content.program_title = title if title else "%s Program" % name
    content.sales_page_key = key if key else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    content.save()
    return content

def add_client_to_blitz(blitz, client):
    """
    Assuming we'll want to attach more info to plan joining
    """
    # for a Provisional 1:1 (recurring) blitz, add client to a copy of the provisional instance
    if blitz.provisional:
        blitz.pk = None
        blitz.provisional = False
        blitz.recurring = True
        blitz.title = "individual: %s" % client.name
        blitz.url_slug = str(client.pk)
        blitz.save()

    membership = BlitzMember.objects.create(blitz=blitz, client=client)
    return membership

# TODO: should be instance method of GymSession
def grouped_sets_with_user_data(gym_session):
    """
    wrapper around (workouts) get_grouped_sets - "sets" is a list of (set, completed_set) tuples
    """
    workout = gym_session.workout_plan_day.workout
    grouped_sets = workout_utils.get_grouped_sets(workout)
    for d in grouped_sets:
        sets = []
        for s in d['sets']:
            try:
                completed_set = CompletedSet.objects.get(gym_session=gym_session, workout_set=s)
            except ObjectDoesNotExist:
                completed_set = None
            sets.append( (s, completed_set) )
        d['sets'] = sets

    return grouped_sets

def JSONResponse(content):
    return HttpResponse(json.dumps(content), mimetype="application/json")


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

def get_client_summary_html(client, macro_goals, macro_history):
    macro_goals_formatted = { k: '{:.2f}'.format(macro_goals[k]/1000.00) for k in macro_goals }
    return render_to_string('dashboard/client_summary.html', {
        'client': client,
        'macro_goals': macro_goals_formatted,
        'macro_history': macro_history,
        'MEDIA_URL': MEDIA_URL
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


