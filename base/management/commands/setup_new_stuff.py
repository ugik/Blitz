from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User

from base.models import Client, Trainer, Blitz, BlitzMember, BlitzInvitation, MacroDay, TrainerAlert
from workouts.models import Lift, Workout, WorkoutSet, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay
from base.utils import create_trainer, create_client, add_client_to_blitz
from base.new_content import create_new_parent_comment, add_child_to_comment, add_like_to_comment
from base import new_content
from base.simulations import knicks_profile, simulate_blitz_through_date
from workouts import utils as workout_utils
from base import alerts

import datetime
import csv

class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone_now()
        most_recent_monday = now.date() - datetime.timedelta(days=now.weekday())
        blitz_start_date = most_recent_monday - datetime.timedelta(days=14)

#        import pdb; pdb.set_trace()

        mikerashid = Trainer
        mikerashid_plan = WorkoutPlan
        try:
            mikerashid = Trainer.objects.get(name='Mike Rashid')
        except Trainer.DoesNotExist:
            mikerashid = create_trainer("Mike Rashid", "mr@example.com", "asdf")
            mikerashid.headshot_from_image(settings.TEST_MEDIA_DIR + '/mike-rashid.jpg')
            mikerashid.short_name = "Mike"
            mikerashid.save()

        try:
            mikerashid_plan = WorkoutPlan.objects.get(name='Mike Rashid Plan')
        except WorkoutPlan.DoesNotExist:

            mikerashid_plan = workout_utils.load_workout_plan_from_fileset_2(
                "Mike Rashid Plan",
                settings.DATA_DIR + '/mikerashid/workout-meta.csv',
                settings.DATA_DIR + '/mikerashid/workouts.csv',
                settings.DATA_DIR + '/mikerashid/plan.csv',)

        blitz = Blitz
        try:
            blitz = Blitz.objects.get(url_slug='mike')
        except Blitz.DoesNotExist:
            content = create_salespagecontent("Heavy", mikerashid)
            blitz = Blitz.objects.create(trainer=mikerashid, workout_plan=mikerashid_plan,
                title="Make it HEAVY", begin_date=blitz_start_date, url_slug="mike")
            blitz.sales_page_content = content
            blitz.uses_macros = True
            blitz.macro_strategy = 'M'
            blitz.price = 1
            blitz.save()

        luke = Client
        try:
            luke = Client.objects.get(name='Luke Walton')
        except Client.DoesNotExist:
            luke = create_client("Luke Walton", "luke@example.com", "asdf", 29, 230, 6, 10, 'M')
            luke.headshot_from_image(settings.TEST_MEDIA_DIR + '/luke_walton.jpg')
            add_client_to_blitz(blitz, luke)

        tay = Client
        try:
            tay = Client.objects.get(name='Tayshawn Prince')
        except Client.DoesNotExist:
            tay = create_client("Tayshawn Prince", "tay@example.com", "asdf", 35, 200, 6, 9, 'M')
            tay.headshot_from_image(settings.TEST_MEDIA_DIR + '/tayshaun_prince.png')
            add_client_to_blitz(blitz, tay)


        clients = [luke, tay]

        # seed some demo workout data
        shapeness = knicks_profile()
        for d in clients:
            simulate_blitz_through_date(blitz, d, timezone_now().date(), shapeness)
            d.has_completed_intro = True
            d.save()

        for client in clients:
            for date, day in blitz.iterate_workouts():
                if date >= timezone_now().date(): break
                alerts.create_alerts_for_day(client, date)


        # comments
        lukeburr = create_new_parent_comment(luke.user, "Who wants to go get a burrito?", timezone_now())[0]
        add_like_to_comment(lukeburr, tay.user, timezone_now())

        mrcomment = create_new_parent_comment(mikerashid.user, "Hey boys", timezone_now())[0]

        add_child_to_comment(lukeburr, luke.user, "Sure buddy", timezone_now())
        noburr = add_child_to_comment(lukeburr, mikerashid.user,
            "No TexMex, get a clue!", timezone_now())


