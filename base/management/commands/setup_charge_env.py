from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User

from base.models import Client, Trainer, Blitz, BlitzMember, BlitzInvitation, MacroDay, TrainerAlert
from workouts.models import Lift, Workout, WorkoutSet, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay
from base.utils import create_trainer, create_client, add_client_to_blitz, create_salespagecontent
from base.new_content import create_new_parent_comment, add_child_to_comment, add_like_to_comment
from base import new_content
from workouts import utils as workout_utils
from base import alerts

from base.models import Client, Trainer, Blitz, SalesPageContent, BlitzMember, BlitzInvitation
from workouts.models import WorkoutSet, Lift, Workout, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay, Exercise, ExerciseCustom, WorkoutSet, WorkoutSetCustom

from django.utils.timezone import now as timezone_now, get_current_timezone as current_tz
from pytz import timezone
from django.db.models import Q

import os
import xlrd
import datetime
import requests
from datetime import date, timedelta
from random import randint

class Command(BaseCommand):

    def handle(self, *args, **options):

        timezone = current_tz()
        back = randint(100,300)    # random # of days
        startdate = date.today() - timedelta(days = back)
        print startdate


