from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User

from base.models import Client, Trainer, Blitz, BlitzMember, BlitzInvitation, MacroDay, TrainerAlert
from workouts.models import Lift, Workout, WorkoutSet, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay
from base.utils import create_trainer, create_client, add_client_to_blitz, create_salespagecontent
from base.new_content import create_new_parent_comment, add_child_to_comment, add_like_to_comment
from base import new_content
from base.simulations import knicks_profile, simulate_blitz_through_date, simulate_recurring_blitz
from workouts import utils as workout_utils
from base import alerts

import datetime
from dateutil import rrule
from datetime import date, timedelta
import csv
from random import randint

class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone_now()
        most_recent_monday = now.date() - datetime.timedelta(days=now.weekday())
        blitz_start_date = most_recent_monday - datetime.timedelta(days=14)

#        import pdb; pdb.set_trace()

        troy = Trainer
        troy_plan = WorkoutPlan
        try:
            troy = Trainer.objects.get(short_name='troy')
        except Trainer.DoesNotExist:
            troy = create_trainer("Troy Polamalu", "troy@example.com", "asdf")
            troy.short_name = "troy"
            troy.save()

        try:
            troy_plan = WorkoutPlan.objects.get(name='Troy 1-week')
        except WorkoutPlan.DoesNotExist:

            troy_plan = workout_utils.load_workout_plan_from_fileset_2(
                "Troy 1-week",
                settings.DATA_DIR + '/mikerashid/workout-meta.csv',
                settings.DATA_DIR + '/mikerashid/workouts.csv',
                settings.DATA_DIR + '/mikerashid/plan.csv',)

        troy_plan.trainer = troy
        troy_plan.save()

        blitz = Blitz

        try:
            blitz = Blitz.objects.get(url_slug='TroyTime')
        except Blitz.DoesNotExist:
            content = create_salespagecontent("3 Week Troy Plan", troy)
            blitz = Blitz.objects.create(trainer=troy, workout_plan=troy_plan,
                title="Troy Time", begin_date=blitz_start_date, url_slug="TroyTime")
            blitz.provisional = False
            blitz.recurring = True
            blitz.group = True
            blitz.free = True
            blitz.sales_page_content = content
            blitz.uses_macros = True
            blitz.macro_strategy = 'M'
            blitz.save()

        for x in range(1, 100):   # lots of open group clients
            c = Client
            name = "Client%s" % x
            email = "Client%s@example.com" % x
            try:
                c = Client.objects.get(name=name)
            except Client.DoesNotExist:
                c = create_client(name, email, "asdf", 29, 230, 6, 10, 'M')
            add_client_to_blitz(blitz, c)

            comment = create_new_parent_comment(c.user, "Sample comment #%s" % x, timezone_now())[0]
            add_like_to_comment(comment, c.user, timezone_now())



