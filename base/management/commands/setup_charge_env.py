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
import balanced

import os
import xlrd
import datetime
from dateutil import rrule
import requests
from datetime import date, timedelta
from random import randint

class Command(BaseCommand):

    def handle(self, *args, **options):

        # sample charge card
        card = balanced.Card(
            cvv='123',
            expiration_month='12',
            number='5105105105105100',
            expiration_year='2020'
            ).save()
        cc = balanced.Card.fetch(card.href)

        clients = ['Dwayne Wade', 'Richard Hamilton', 'Leon Powe', 'Manute Bol', 'Spud Webb', 
                   'Dennis Rodman', 'Nate Robinson', 'Manu Ginobili', 'David Robinson', 'Ray Allen']
        timezone = current_tz()
        data = []
        for client in clients:
            back = randint(100,500)    # random # of days
            startdate = date.today() - timedelta(days = back)
            data.append({'name': client, 'start': startdate})

        print "Test data for payments history (today is %s)" % date.today()
        
        for d in data:
            blitz = Blitz.objects.get(url_slug='3weeks')
            m = (len(list(rrule.rrule(rrule.MONTHLY, dtstart=d['start'], until=date.today()))))

            c = create_client(d['name'], "%s@example.com" % d['name'].split(' ', 1)[0].lower(), "asdf", randint(22,35), randint(180,230), 6, randint(0,11), 'M')
            c.balanced_account_uri = card.href
            c.save()

            add_client_to_blitz(blitz, c, None, blitz.price, d['start'])

            # charge a partial amount for each client
            meta = {"client_id": c.pk, "blitz_id": blitz.pk, 'email': c.user.email}
            payment = randint(1,3)*blitz.price*100
            debit = cc.debit(appears_on_statement_as = 'Blitz.us test', amount = payment, 
                             description='Blitz.us test', meta = meta)

            print d['name'], "%s@example.com" % d['name'].split(' ', 1)[0].lower(), " Start:"+str(d['start']), " # months"+str(m), "Charge: (cents)"+str(payment)


