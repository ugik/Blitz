'''
Structure for SalesPages, Trainers, Blitzes and WorkoutPlans:

Trainers:
Each Trainer (T) has (1-n) Sales Pages (S)
Each T defines a unique top-level URL, eg. Blitz.us/jc-deen

Sales Pages:
Each S is either for 1:1 "individual" Client (C) or Group of Clients, we'll refer to these as Si and Sg
Each Si has exactly one individual Blitz (Bi), it is copied onto each new C upon signup
Each Sg has (1-n) Group Blitz(es) (Bg), each Bg is shared by C's in the group
Each S defines a trainer-unique 2nd-level URL, eg. Blitz.us/jc-deen/ripped

Blitzes:
Bi's are recurring monthly billing, continuously loop through their program weeks
Bg's are one-time billing, start-end period, C's can only join prior to start date
From Programs tab a T can create a new Bg, associated with a new or existing Sg
Before the (Bi, Bg) begins the T assigns a WP to it
After a Bg ends, its data will be deleted, some of its artifacts may be lifted onto its Sg

WorkoutPlans:
Each T develops (1-n) Workout Plans (WP) (created with helpers)
A WP defines weekly/daily exercises for all C's on the B
Each B has exactly one WP

Clients:
A Client (C) signs up via S, sign-up can be before a program is associated with a (Bi, Bg)
Once a C signs up, the T is notified
T can swap WP for a Bi and its individual C
T can customize a WP for a C on a B (via helpers)
_________

Client signup scenario (a): individual client (most typical)
    C signs up via Si to Bi and its WP, pays monthly

Client signup scenario (b): group of clients
    C signs up via Sg to Bg and its WP, pays one-time fee

extension of scenario (b)
Client signup scenario (c): group from Group Sales Page with multiple Blitz Groups
   C signs up via Sg to Bg3 and its WP as Bg1 and Bg2 were full or already started
'''

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.utils.timezone import now as timezone_now, get_current_timezone as current_tz

from base.templatetags import units_tags

from workouts.models import WorkoutPlanDay, WorkoutSet, WorkoutPlan, DAYS_OF_WEEK

import datetime
import random
import string
from PIL import Image, ImageOps
import StringIO
from pytz import timezone
import json
import itertools

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unspecified'),
)

UNIT_CHOICES = (
    ('M', 'Metric'),
    ('I', 'Imperial'),
)

FEE_CHOICES = (('O', 'One-time',), ('R', 'Recurring',))

#
# This is junk here; going to replace this all with a new custom user model instead but dont feel like
# figuring out now
#

# return date for next specified weekday (Monday=0), inclusive of date provided
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def user_type(user):
    try:
        user.trainer
        return 'T'
    except ObjectDoesNotExist:
        pass

    try:
        user.client
        return 'D'
    except:
        raise Exception("No type for user")

def user_display_name(user):
    """
    Display name of a user, whether trainer or client
    """
    try:
        return user.trainer.name
    except ObjectDoesNotExist:
        pass

    try:
        return user.client.name
    except:
        raise Exception("Cannot display user")

def user_headshot_url(user):
    try:
        return user.trainer.get_headshot_url()
    except ObjectDoesNotExist:
        pass

    try:
        return user.client.get_headshot_url()
    except:
        raise Exception("No headshot for user")

def user_blitz(user):
    try:
        return user.trainer.get_blitz()
    except ObjectDoesNotExist:
        pass

    try:
        return user.client.get_blitz()
    except:
        raise Exception("No blitz for user")

def user_is_trainer(user):
    return user_type(user) == 'T'

def get_profile_url(user):
    if user_is_trainer(user):
        return "/"
    else:
        return reverse('client_profile', args=(user.client.pk,))

def get_timezone(user):
    try:
        return user.trainer.get_timezone()
    except ObjectDoesNotExist:
        pass

    try:
        return user.client.get_timezone()
    except:
        raise Exception("No blitz for user")

def get_current_datetime(user):
    try:
        return user.trainer.current_datetime()
    except ObjectDoesNotExist:
        pass

    try:
        return user.client.current_datetime()
    except:
        raise Exception("No blitz for user")

def forgot_password_token(user):
    try:
        return user.trainer.forgot_password_token
    except ObjectDoesNotExist:
        pass

    try:
        return user.client.forgot_password_token
    except:
        raise Exception("No blitz for user")

User.user_type = property(lambda u: user_type(u))
User.is_trainer = property(lambda u: user_is_trainer(u))
User.display_name = property(lambda u: user_display_name(u))
User.headshot_url = property(lambda u: user_headshot_url(u))
User.blitz = property(lambda u: user_blitz(u))
User.get_profile_url = property(lambda u: get_profile_url(u))
User.timezone = property(lambda u: get_timezone(u))
User.current_datetime = property(lambda u: get_current_datetime(u))
User.forgot_password_token = property(lambda u: forgot_password_token(u))


class Trainer(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, default="")
    short_name = models.CharField(max_length=10, default="")
    headshot = models.ImageField(upload_to="headshots/", blank=True, null=True)
    external_headshot_url = models.CharField(max_length=1000, default="", blank=True)
    timezone = models.CharField(max_length=40, default='US/Pacific')
    date_created = models.DateField(default=datetime.date.today)

    forgot_password_token = models.CharField(max_length=40, default="")

    # HACK - move to session var
    currently_viewing_blitz = models.ForeignKey('base.Blitz', null=True, blank=True, related_name="currently_viewing_trainer")

    def __unicode__(self):
        return self.name

    def get_blitz(self):
        if self.currently_viewing_blitz:
            return self.currently_viewing_blitz
        else:
            return self.active_blitzes()[0]

    def get_headshot_url(self):
        if self.headshot:
            return self.headshot.url
        elif self.external_headshot_url:
            return self.external_headshot_url
        else:
            return settings.STATIC_URL + 'images/silhouette.jpeg'

    def headshot_from_image(self, image_path):
        image = Image.open(image_path)
        size = (75, 75)
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS)

        thumb_io = StringIO.StringIO()
        thumb.save(thumb_io, format='JPEG')
        thumb_contentfile = ContentFile(thumb_io.getvalue())

        filename = image_path.split('/')[-1]
        self.headshot.save(filename, thumb_contentfile)

    def get_timezone(self):
        return timezone(self.timezone)

    def current_datetime(self):
        return self.get_timezone().normalize(timezone_now())

    def get_alerts(self):
        alerts = self.traineralert_set.filter(trainer_dismissed=False).order_by('-date_created')
        return [a for a in alerts]
        # return [a for a in alerts if a.is_still_relevant()]

<<<<<<< HEAD
    def active_blitzs(self):
        # return self.blitz_set.all().exclude(provisional=True)
=======
    def active_blitzes(self):
#        return self.blitz_set.all().exclude(provisional=True)
>>>>>>> 34b3097aae896ddf40b81bcf9ceda81a577c3568
        return self.blitz_set.all()

    def set_currently_viewing_blitz(self, blitz):
        self.currently_viewing_blitz = blitz
        self.save()
    
    def all_clients(self):
        members = [f.members() for f in self.active_blitzes()]
        return list(itertools.chain(*members))

    def _all_clients(self):
        clients = Client.objects.get_empty_query_set()

        for b in self.active_blitzs():
            clients |= b._members()

        return clients

    def feed_items(self):
        blitzes = self.blitz_set.all()
        return len(blitzes[0].feeditem_set.all())

    def multiple_blitzes(self):
#        return self.blitz_set.all().exclude(provisional=True).count() > 1
        return self.blitz_set.all().count() > 1

class Client(models.Model):

    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, default="")
    short_name = models.CharField(max_length=100, default="")
    age = models.IntegerField(null=True, blank=True)
    weight_in_lbs = models.IntegerField(null=True, blank=True)
    height_feet = models.IntegerField(null=True, blank=True)
    height_inches = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U", blank=True)
    headshot = models.ImageField(upload_to="headshots/", blank=True, null=True)
    external_headshot_url = models.CharField(max_length=1000, default="", blank=True)
    timezone = models.CharField(max_length=40, default='US/Pacific')
    has_completed_intro = models.BooleanField(default=False)
    macro_target_json = models.TextField(default="", blank=True)

    forgot_password_token = models.CharField(max_length=40, default="")

    units = models.CharField(max_length=1, choices=UNIT_CHOICES, default="I", blank=True)
    date_created = models.DateField(default=datetime.date.today)

    # payment
    balanced_account_uri = models.CharField(max_length=200, default="", blank=True)

    def __unicode__(self):
        return self.name

    def get_blitz(self):
        """
        Client has exactly one blitz
        """
        return self.blitz_membership().blitz

    def blitz_membership(self):
        return BlitzMember.objects.get(client=self)

    def other_blitz_members(self):
        """
        Again, only works because exactly one blitz
        """
        memberships = BlitzMember.objects.filter(blitz=self.get_blitz())
        return [m.client for m in memberships if m.client != self]

    def get_headshot_url(self):

        if self.headshot:
            return self.headshot.url
        elif self.external_headshot_url:
            return self.external_headshot_url
        else:
            return settings.STATIC_URL + 'images/silhouette.jpeg'

    def get_todays_workout(self, timezone=None):
        if timezone is None:
            timezone = current_tz()
        weekday_index = timezone.normalize(timezone_now()).date().weekday()
        return self.get_blitz().get_workout_for_day(self.get_blitz().current_week(), DAYS_OF_WEEK[weekday_index][0])

    def get_next_workout(self, timezone=None):
        """
        (date, day) tuple of next workout
        is today's workout even if already completed
        """
        if timezone is None:
            timezone = current_tz()
        today = timezone.normalize(timezone_now()).date()
        for workout_date, workout_plan_day in self.get_blitz().iterate_workouts():
            if workout_date >= today and not GymSession.objects.filter(client=self, workout_plan_day=workout_plan_day, is_logged=True).exists():
                return workout_date, workout_plan_day
        return None, None

    def get_missed_workouts(self, timezone=None):
        if not self.get_blitz().workout_plan:
            return []
        if timezone is None:
            timezone = current_tz()
        today = timezone.normalize(timezone_now()).date()
        ret = []
        for workout_date, workout_plan_day in self.get_blitz().iterate_workouts():
            if workout_date < today and not GymSession.objects.filter(client=self, workout_plan_day=workout_plan_day, is_logged=True).exists():
                ret.append( (workout_date, workout_plan_day) )
            elif workout_date >= today:
                break
        return ret

    def has_workout_today(self, timezone=None):
        return self.get_todays_workout(timezone) is not None

    def headshot_from_image(self, image_path):
        image = Image.open(image_path)
        size = (75, 75)
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS)

        thumb_io = StringIO.StringIO()
        thumb.save(thumb_io, format='JPEG')
        thumb_contentfile = ContentFile(thumb_io.getvalue())

        filename = image_path.split('/')[-1]
        self.headshot.save(filename, thumb_contentfile)

    def get_gym_sessions(self):
        """
        Gym sessions in chronological order
        """
        return self.gymsession_set.all().order_by('date_of_session')

    def get_feeditems(self):
        """
        Feed items in chronological order
        """

        feeditems = FeedItem.objects.get_empty_query_set()
       
        # Adds client related Gym Sessions to the feeditems query set
        for q in self.gymsession_set.all():
            feeditems |= q.feeditems.all()

        # Adds client related Comments to the feeditems query set
        for q in Comment.objects.filter(user=self.user).all():
            feeditems |= q.feeditems.all()

        return feeditems

    def get_gym_sessions_reverse(self):
        """
        Gym sessions, most recent first
        """
        return self.gymsession_set.all().order_by('-date_of_session')

    def lift_summary(self, lift):

        ret = {
            'has_completed': CompletedSet.objects.filter(gym_session__client=self).exists(),
        }
        if ret['has_completed']:
            for gym_session in self.get_gym_sessions_reverse():
                if CompletedSet.objects.filter(gym_session=gym_session, workout_set__lift=lift).exists():
                    ret['last_session'] = CompletedSet.objects.filter(gym_session=gym_session, workout_set__lift=lift)
                    break
        return ret

    def get_timezone(self):
        return timezone(self.timezone)

    def current_datetime(self):
        return self.get_timezone().normalize(timezone_now())

    def macro_target_for_date(self, date):
        spec = self.macro_target_spec()
        if spec:
            if self.get_blitz().get_workout_for_date(date):
                return {
                    'calories': {'min': spec['training_calories_min'], 'max': spec['training_calories'] },
                    'protein': {'min': spec['training_protein_min'], 'max': spec['training_protein'] },
                    'carbs': {'min': spec['training_carbs_min'], 'max': spec['training_carbs'] },
                    'fat': {'min': spec['training_fat_min'], 'max': spec['training_fat'] },
                }
            else:
                return {
                    'calories': {'min': spec['rest_calories_min'], 'max': spec['rest_calories'] },
                    'protein': {'min': spec['rest_protein_min'], 'max': spec['rest_protein'] },
                    'carbs': {'min': spec['rest_carbs_min'], 'max': spec['rest_carbs'] },
                    'fat': {'min': spec['rest_fat_min'], 'max': spec['rest_fat'] },
                }

    def current_macro_target(self):
        return self.macro_target_for_date(self.current_datetime().date())

    def macro_target_spec(self):
        if self.macro_target_json:
            return json.loads(self.macro_target_json)

    def macros_set(self):
        return bool(self.macro_target_json)

    def current_blitz_week(self):
        return self.get_blitz().current_week(self.get_timezone())

    def current_blitz_day(self):
        return self.get_blitz().current_day(self.get_timezone())

    def current_blitz_day_index(self):
        return self.get_blitz().current_day_index(self.get_timezone())

MACRO_STRATEGIES = (
    ('M', 'Macros Only'),
    ('C', 'Calories Only'),
    ('B', 'Both Macros And Calories'),
    ('N', 'N/A'),
)

class Blitz(models.Model):
# /trainer.short_name resolves to trainer id, which ties to 1-n SalesPages
# /trainer.short_name/blitz.url_slug resolves to specific blitz

    url_slug = models.SlugField(max_length=25, default="")
    trainer = models.ForeignKey(Trainer)
    recurring = models.BooleanField(default=False) # Recurring blitzes repeat over time
    provisional = models.BooleanField(default=False) # True for initial 1:1 Blitzes
    sales_page_content = models.ForeignKey('base.SalesPageContent', null=True)

    # workout_plan is optional, a Blitz without one is provisional
    workout_plan = models.ForeignKey(WorkoutPlan, blank=True, null=True)

    # this is monday of week 1, model.save() will adjust as necessary
    begin_date = models.DateField()

    # calculated from length of plan if null
    custom_end_date = models.DateField(null=True, blank=True)
    custom_price_per_workout = models.FloatField(null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)
    to_expect_text = models.TextField(default="", blank=True)

    # macros
    uses_macros = models.BooleanField(default=False)
    macro_strategy = models.CharField(max_length=1, default="", choices=MACRO_STRATEGIES)

    # payment
    price = models.IntegerField(default=0)
    price_model = models.CharField(max_length=1, choices=FEE_CHOICES, default="R", blank=True)

    def save(self, *args, **kwargs):
#        if self.urlkey == "":
#            self.urlkey = ''.join(random.choice(string.digits) for x in range(6))
        # make sure begin_date is a Monday
        self.begin_date = next_weekday(self.begin_date, 0)

        super(Blitz, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    # WEEK IS 1-INDEXED
    def current_week(self, timezone=None):
        if timezone is None:
            timezone = current_tz()
        return 1 + (timezone.normalize(timezone_now()).date() - self.loop_begin_date()).days / 7

    def current_day_index(self, timezone=None):
        if timezone is None:
            timezone = current_tz()
        return timezone.normalize(timezone_now()).date().weekday()

    def current_day(self, timezone=None):
        return DAYS_OF_WEEK[self.current_day_index(timezone)][0]

    def in_progress(self, timezone=None):
        if timezone is None:
            timezone = current_tz()
        return self.begin_date <= timezone.normalize(timezone_now()).date() < self.loop_begin_date() + datetime.timedelta(weeks=self.num_weeks() )

    def get_workout_for_day(self, week, day):
        try:
            week = self.workout_plan.workoutplanweek_set.get(week=week)
            day = week.workoutplanday_set.get(day_of_week=day)
            return day
        except ObjectDoesNotExist:
            return None

    def get_workout_for_date(self, date):
        week, day = self.get_day_for_date(date)
        try:
            week = self.workout_plan.workoutplanweek_set.get(week=week)
            day = week.workoutplanday_set.get(day_of_week=day)
            return day
        except ObjectDoesNotExist:
            return None

    def get_workout_date(self, week, day):
        days_offset = (week-1)*7
        days_offset += next(i for i, d in enumerate(DAYS_OF_WEEK) if d[0] == day)
        return self.loop_begin_date() + datetime.timedelta(days=days_offset)

    def get_date_for_day_index(self, week, day_index):
        days_offset = (week-1)*7
        days_offset += day_index
        return self.loop_begin_date() + datetime.timedelta(days=days_offset)

    def get_day_for_date(self, date):
        week = 1 + (date - self.loop_begin_date()).days / 7
        day_index = (date - self.loop_begin_date()).days % 7
        return week, DAYS_OF_WEEK[day_index][0]

    def iterate_workouts(self):
        """
        iter of (date, workoutplanday) tuples
        """
        for workout_plan_day in self.workout_plan.iterate_days():
            yield ( self.get_workout_date(workout_plan_day.workout_plan_week.week, workout_plan_day.day_of_week), workout_plan_day )

    def members(self):
        return [f.client for f in self.blitzmember_set.all()]

    def _members(self):
        members = Client.objects.get_empty_query_set()
        for b in self.blitzmember_set.all():
            members |= Client.objects.filter(pk=b.client.pk)

        return members

    def end_date(self): # the date of last workout
        if self.custom_end_date:
            return self.custom_end_date
        if self.recurring:
            return self.loop_end_date()
        if self.provisional: 
            return self.begin_date
        if not list(self.iterate_workouts()):
            return self.begin_date    # TODO resolve end-date that hasn't been set yet
        return list(self.iterate_workouts())[-1][0]

# loop begin/end dates connote the dates of repeating Blitz (for 1:1 Clients) per today's date
    def loop_begin_date(self, timezone=None):
        if not self.recurring:   # ignore for non-recurring Blitz
            return self.begin_date

        if timezone is None:
            timezone = current_tz()
            timezone.normalize(timezone_now()).date()

        period_begin = self.begin_date
        # loop through Blitz period to encompass today's date
        while period_begin + datetime.timedelta(days=7*self.num_weeks()) <= timezone.normalize(timezone_now()).date():
            period_begin += datetime.timedelta(days=7*self.num_weeks())

        return next_weekday(period_begin,0)

    def loop_end_date(self, timezone=None): 
        return self.loop_begin_date() + datetime.timedelta(days=7*self.num_weeks())

    def num_weeks(self):
        return self.workout_plan.workoutplanweek_set.all().count()

    def price_per_week(self):
        return float(self.price) / self.num_weeks()

    def num_workouts(self):
        return len(list(self.iterate_workouts()))

    def price_per_workout(self):
        if self.custom_price_per_workout:
            return int(self.custom_price_per_workout)
        if self.provisional: 
            return 0
        return float(self.price) / self.num_workouts()

    def days_since_begin(self, timezone=None):
        if timezone is None:
            timezone = current_tz()
        today = timezone.normalize(timezone_now()).date()
        delta = today - self.begin_date
        return delta.days

    def active_users(self):
        """
        All Users that are active in this blitz
        Includes users for all clients and trainers
        """
        users = []
        for f in self.blitzmember_set.all():
            users.append(f.client.user)
        users.append(self.trainer.user)
        return users

class BlitzInvitation(models.Model):

    blitz = models.ForeignKey(Blitz)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    signup_key = models.CharField(max_length=30, default="")

    def __unicode__(self):
        return "Invitation for %s; key: %s" % (self.name, self.signup_key)

class BlitzMember(models.Model):

    client = models.ForeignKey(Client)
    blitz = models.ForeignKey(Blitz)
    date_created = models.DateField(default=datetime.date.today)

    def __unicode__(self):
        return "%s enrolled in %s" % (str(self.client), str(self.blitz))


class FeedItem(models.Model):

    blitz = models.ForeignKey(Blitz)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return "Feed item for %s / %d in blitz %s" % ( str(self.content_type), self.object_id, str(self.blitz) )


class GymSession(models.Model):
    """
    One session at the gym, as part of a workout plan
    Cannot be used for a generic gym session, yet...
    """

    date_of_session = models.DateField()
    workout_plan_day = models.ForeignKey(WorkoutPlanDay)
    client = models.ForeignKey(Client)
    notes = models.TextField(default="")
    is_logged = models.BooleanField(default=False)
    feeditems = generic.GenericRelation(FeedItem, related_name='gymsessions')

    def __unicode__(self):
        return "%s lifted on %s" % (str(self.client), str(self.date_of_session))

    def save_exercises_to_file(self, filename):
        """
        Saves the exercises in this gym session to a text file
        One CompletedSet per line, each line has fields:
            workout_set.lift.slug  num_reps_completed  weight_in_lbs
        Assume multiple sets for a lift are in order
        """
        f = open(filename, 'w')
        for completed_set in self.completedset_set.all().order_by('workout_set__lift', 'workout_set__order'):
            fields = [
                completed_set.workout_set.lift.slug,
                str(completed_set.num_reps_completed),
                str(completed_set.weight_in_lbs),
            ]
            f.write('\t'.join(fields) + '\n')
        f.close()

    def has_likes(self):
        return self.gymsessionlike_set.all().count() > 0

    def users_that_like(self):
        return [c.user for c in self.gymsessionlike_set.all()]

    def liked_by_user(self, user):
        return user in self.users_that_like()

    def comments(self):
        return self.gymsessioncomments.all()

SET_TYPES = (
    ('S', 'Standard'),
    ('W', 'Weighted'),
    ('B', 'Body Weight'),
    ('A', 'Assisted'),
)

class CompletedSet(models.Model):
    """
    One set that a client actually did
    """
    gym_session = models.ForeignKey(GymSession)
    workout_set = models.ForeignKey(WorkoutSet)
    num_reps_completed = models.IntegerField()
    weight_in_lbs = models.FloatField(null=True)
    set_type = models.CharField(max_length=1, choices=SET_TYPES, default='S')

    def save(self, *args, **kwargs):
        self.weight_in_lbs = units_tags.kg_conversion(self.weight_in_lbs, self.gym_session.client)
        super(CompletedSet, self).save(*args, **kwargs)

    def ratio_of_pr(self):
        maxset = CompletedSet.objects.filter(gym_session__client=self.gym_session.client, workout_set__lift=self.workout_set.lift).order_by('-weight_in_lbs')[0]
        if maxset.weight_in_lbs > 0:
            return self.weight_in_lbs / maxset.weight_in_lbs
        else:
            return 0

    def no_weight(self):
        if weight_in_lbs == 0:
            return True
        else:
            return False

    def reverse_ratio_of_pr(self):
        return 1-self.ratio_of_pr()

    def __unicode__(self):
        return "%s / %s / %s" % (
            self.display_str(),
            self.workout_set.lift.slug, 
            str(self.gym_session),
        )


class CheckIn(models.Model):

    client = models.ForeignKey(Client)
    weight = models.IntegerField(null=True, blank=True)
    front_image = models.ImageField(upload_to="checkins/", blank=True, null=True)
    side_image = models.ImageField(upload_to="checkins/", blank=True, null=True)
    date_created = models.DateField(default=datetime.date.today)

    def __unicode__(self):
        return "Check-in %s: \"%s\"" % (self.client.name, self.date_created)

    def days_since_checkin(self, date=None, timezone=None):
        if timezone is None:
            timezone = current_tz()
        today = timezone.normalize(timezone_now()).date()
        delta = today - self.date_created
        return delta.days


class Comment(models.Model):

    user = models.ForeignKey(User)
    text = models.TextField()
    image = models.ImageField(upload_to="feed/", blank=True, null=True)
    date_and_time = models.DateTimeField()
    parent_comment = models.ForeignKey('self', null=True, blank=True)
    gym_session = models.ForeignKey(GymSession, null=True, blank=True, related_name='gymsessioncomments')
    feeditems = generic.GenericRelation(FeedItem)

    def __unicode__(self):
        return "%s: \"%s\"" % (self.user.display_name, self.text)

    def comments(self):
        return self.comment_set.all()

    def has_likes(self):
        return self.commentlike_set.all().count() > 0

    def users_that_like(self):
        return [c.user for c in self.commentlike_set.all()]

    def liked_by_user(self, user):
        return user in self.users_that_like()

    def plain_text(self):
        return self.text

    def parent_absolute_url(self):
        if self.gym_session:
            parent = self.gym_session
        elif self.parent_comment:
            parent = self.parent_comment
        else:
            parent = self
        content_type = ContentType.objects.get_for_model(parent)
        feed_item = FeedItem.objects.get(content_type=content_type, object_id=parent.pk)
        if self.gym_session:
            return '/post/gym/%d' % feed_item.pk
        else:
            return '/post/comment/%d' % feed_item.pk

class CommentLike(models.Model):

    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment, null=True, blank=True)
    date_and_time = models.DateTimeField()

    def __unicode__(self):
        return "%s liked \"%s\"" % (self.user.display_name, self.comment)


# TODO: delete and start using generic foreign keys for comments and likes
# so new feed item classes can have both
class GymSessionLike(models.Model):

    user = models.ForeignKey(User)
    gym_session = models.ForeignKey(GymSession, null=True, blank=True)
    date_and_time = models.DateTimeField()

    def __unicode__(self):
        return "%s liked \"%s\"" % (self.user.display_name, self.gym_session)


class MacroDay(models.Model):

    client = models.ForeignKey(Client)
    day = models.DateField()
    protein = models.NullBooleanField()
    carbs = models.NullBooleanField()
    fat = models.NullBooleanField()
    calories = models.NullBooleanField()

    def __unicode__(self):
        return "Macro for %s on %s" % (self.client, self.day)

    def num_pass(self):
        return (1 if self.protein else 0) + (1 if self.carbs else 0) + (1 if self.fat else 0) + (1 if self.calories else 0)

    def num_total(self):
        return (1 if self.protein is not None else 0) + (1 if self.carbs is not None else 0) + (1 if self.fat is not None else 0) + (1 if self.calories is not None else 0)

    def toJSON(self):
        return {
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'calories': self.calories,
            'all_pass': self.protein is True and self.carbs is True and self.fat is True and self.calories is True,
            'all_fail': self.protein is False and self.carbs is False and self.fat is False and self.calories is False,

            'month': self.day.month,
            'day': self.day.day,
            'year': self.day.year,
            'second_person_description': self.second_person_description(),
        }

    def second_person_description(self):
        num_pass = self.num_pass()
        num_total = self.num_total()
        if num_pass == 4:
            return "You hit all your macros. Nice work!"
        elif num_pass == 0:
            return "Missed all your macros? Just call it a cheat day and get back on it tomorrow."
        elif num_pass == 3:
            return "Three out of four ain't bad!"
        elif num_pass == 2:
            return "Two out of four is a start. Get 3 tomorrow. "
        elif num_pass == 1:
            return "You hit only one of your macros. Try harder tomorrow."
        else:
            return "You ate some shit."

TRAINER_ALERT_TYPES = (
    ('W', 'Missed workout'),
    ('M', 'Missed macros for 3 days'),
    ('C', "Haven't commented"),
    ('X', 'Misc. alert')
)

class TrainerAlert(models.Model):

    alert_type = models.CharField(max_length=1, choices=TRAINER_ALERT_TYPES)
    trainer = models.ForeignKey(Trainer)
    client = models.ForeignKey(Client)
    date_created = models.DateField()
    trainer_dismissed = models.BooleanField(default=False)
    text = models.CharField(max_length=100, blank=True, null=True, default="")

    # type specific fields
    workout_plan_day = models.ForeignKey(WorkoutPlanDay, null=True)

    def __unicode__(self):
        return "Alert for %s about %s; reason: %s" % (str(self.trainer), str(self.client), self.alert_type)

    def is_still_relevant(self):
        if self.alert_type == 'W':
            return not GymSession.objects.filter(client=self.client, workout_plan_day=self.workout_plan_day).exists()
        elif self.alert_type == 'X':
            return True
        else:
            return False


class SalesPageContent(models.Model):
# /trainer.short_name resolves to trainer id, which ties to 1-n SalesPages
# /trainer.short_name/blitz.url_slug resolves to specific blitz

    trainer = models.ForeignKey('base.Trainer', null=True)
    group = models.BooleanField(default=False)   # True for Group programs, False for individual
    name = models.CharField(max_length=140, default="", blank=True, null=True)
    url_slug = models.CharField(max_length=30, blank=True, null=True, default="")
    sales_page_key = models.TextField(default="", blank=True, null=True)

    trainer_headshot = models.ImageField(blank=True, null=True, upload_to="headshots/")
    logo = models.ImageField(blank=True, null=True, upload_to="logos/")
    program_title = models.TextField(default="", blank=True, null=True)
    program_introduction = models.TextField(default="", blank=True, null=True)
    program_why = models.TextField(default="", blank=True, null=True)
    program_who = models.TextField(default="", blank=True, null=True)
    program_last_words = models.TextField(default="", blank=True, null=True)

    trainer_note = models.TextField(default="", blank=True, null=True)
    trainer_signature = models.ImageField(blank=True, null=True, upload_to="signatures")
    video_html = models.TextField(default="", blank=True, null=True)
    social_proof_header_html = models.TextField(default="", blank=True, null=True)
    testimonial_1_text = models.TextField(default="", blank=True, null=True)
    testimonial_1_name = models.TextField(default="", blank=True, null=True)
    testimonial_2_text = models.TextField(default="", blank=True, null=True)
    testimonial_2_name = models.TextField(default="", blank=True, null=True)
    testimonial_3_text = models.TextField(default="", blank=True, null=True)
    testimonial_3_name = models.TextField(default="", blank=True, null=True)
    last_ditch_1 = models.TextField(default="", blank=True, null=True)
    last_ditch_2 = models.TextField(default="", blank=True, null=True)

    def __unicode__(self):
        return self.program_title

class Heading(models.Model):
    heading_id = models.CharField(max_length=100, default="")
    short_name = models.CharField(max_length=100, blank=True, null=True, default="")


