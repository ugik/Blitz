from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User

from base.models import Client, Trainer, Blitz, BlitzMember, BlitzInvitation, MacroDay, TrainerAlert
from workouts.models import Lift, Workout, WorkoutSet, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay
from base.utils import create_trainer, create_client, add_client_to_blitz, create_salespagecontent
from base.new_content import create_new_parent_comment, add_child_to_comment, add_like_to_comment
from base import new_content
from base.simulations import knicks_profile, simulate_blitz_through_date
from workouts import utils as workout_utils
from base import alerts

import datetime
import csv
from random import randint

class Command(BaseCommand):

    def handle(self, *args, **options):

        i = new = 0
  
        # update lifts table
        lifts_file = open(settings.DATA_DIR + '/lifts.tsv')
        for line in lifts_file:
            if line.strip() == '' or line.startswith('#'): continue
            fields = line.strip('\n').split('\t')
            if len(fields) == 1:
                fields = line.strip('\n').split(',')
            if len(fields) == 1:
                print "Columns missing in lifts.tsv"
                raise

            lift, created = Lift.objects.get_or_create(slug=fields[0])    
            if created:
                new += 1
                print "new Lift created (%s) %s" % (fields[0],fields[1])

            lift.name = fields[1]
            lift.lift_type = fields[2]
            lift.weight_or_body = (True if fields[3] == "1" else False)
            lift.allow_weight_or_body = (True if fields[4] == "1" else False)
            i += 1

            try: lift.save()
            except: print lift; raise

        print "%s lifts established, %s new" % (i, new)

