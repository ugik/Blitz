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

class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone_now()
        most_recent_monday = now.date() - datetime.timedelta(days=now.weekday())
        blitz_start_date = most_recent_monday - datetime.timedelta(days=14)

        # first set up lifts table
        lifts_file = open(settings.DATA_DIR + '/lifts.tsv')
        for line in lifts_file:
            if line.strip() == '' or line.startswith('#'): continue
            fields = line.strip('\n').split('\t')
            lift = Lift(slug=fields[0], name=fields[1])
            lift.name = fields[1]
            lift.lift_type = fields[2]
            lift.weight_or_body = (True if fields[3] == "1" else False)
            lift.allow_weight_or_body = (True if fields[4] == "1" else False)
            try: lift.save()
            except: print lift; raise

        roglaw = create_trainer("Rog Law", "rog@example.com", "asdf")
        roglaw.headshot_from_image(settings.TEST_MEDIA_DIR + '/rog.png')
        roglaw.short_name = "Rog"
        roglaw.save()

        roglaw_plan = workout_utils.load_workout_plan_from_fileset_2(
            "Mount Sexy",
            settings.DATA_DIR + '/roglaw/workout-meta.csv',
            settings.DATA_DIR + '/roglaw/workouts.csv',
            settings.DATA_DIR + '/roglaw/plan.csv',
            roglaw,
        )
        jc = create_trainer("JC Deen", "jc@example.com", "asdf")
        #jc.headshot_from_image(settings.TEST_MEDIA_DIR + '/rex.jpeg')
        jc.short_name = "jc-deen"
        jc.save()

        ct_plan = workout_utils.load_workout_plan_from_fileset_2(
            "IYMFS",
            settings.DATA_DIR + '/jc/jc-workout-meta.csv',
            settings.DATA_DIR + '/jc/jc-workouts.csv',
            settings.DATA_DIR + '/jc/jc-plan.csv',
            jc,            
        )

        joy = create_trainer("Joy Victoria", "joy@example.com", "asdf")
        joy.headshot_from_image(settings.TEST_MEDIA_DIR + '/joy.png')
        joy.short_name = "Joy"
        joy.save()

        joy_beginner_plan = workout_utils.load_workout_plan_from_fileset_2(
            "Booty-ful Beginnings",
            settings.DATA_DIR + '/joy-beginner/joy-beginner-workout-meta.csv',
            settings.DATA_DIR + '/joy-beginner/joy-beginner-workouts.csv',
            settings.DATA_DIR + '/joy-beginner/joy-beginner-plan.csv',
            joy,
        )
        content = create_salespagecontent("Booty-ful Beginnings", joy)
        joy_beginner_blitz = Blitz.objects.create(trainer=joy, workout_plan=joy_beginner_plan,
            title="Booty-ful Beginnings", begin_date=datetime.date(2013, 5, 20))
        joy_beginner_blitz.sales_page_content = content
        joy_beginner_blitz.url_slug = "joy-victoria-bootyful-beginnings"
        joy_beginner_blitz.uses_macros = True
        joy_beginner_blitz.macro_strategy = 'M'
        joy_beginner_blitz.price = 499
        joy_beginner_blitz.recurring = False
        joy_beginner_blitz.save()

        joy_advanced_plan = workout_utils.load_workout_plan_from_fileset_2(
            "Gluteal Goddess Advanced",
            settings.DATA_DIR + '/joy-advanced/joy-advanced-workout-meta.csv',
            settings.DATA_DIR + '/joy-advanced/joy-advanced-workouts.csv',
            settings.DATA_DIR + '/joy-advanced/joy-advanced-plan.csv',
            joy,
        )
        content = create_salespagecontent("Gluteal Goddess Advanced", joy)
        joy_advanced_blitz = Blitz.objects.create(trainer=joy, workout_plan=joy_advanced_plan,
            title="Gluteal Goddess Advanced", begin_date=datetime.date(2013, 5, 20))
        joy_advanced_blitz.sales_page_content = content
        joy_advanced_blitz.url_slug = "joy-victoria-gluteal-goddess"
        joy_advanced_blitz.uses_macros = True
        joy_advanced_blitz.macro_strategy = 'M'
        joy_advanced_blitz.price = 499
        joy_beginner_blitz.recurring = False
        joy_advanced_blitz.save()

        jahed = create_trainer('Jahed Momand', 'jahedmomand@gmail.com', 'asdf')
        jahed.short_name = "jahed"
        jahed.save()

        jahed_5_day = workout_utils.load_workout_plan_from_fileset_2(
            "Jahed Daily",
            settings.DATA_DIR + '/jahed/workout-meta.csv',
            settings.DATA_DIR + '/jahed/workouts.csv',
            settings.DATA_DIR + '/jahed/plan.csv',
            jahed,
        )


        perryman = create_trainer('Matt Perryman', 'ampedtraining@gmail.com', 'asdf')
        perryman.show_name = "perryman"
        perryman.save()

        perryman_plan = workout_utils.load_workout_plan_from_fileset_2(
            "Perryman",
            settings.DATA_DIR + '/perryman/workout-meta.csv',
            settings.DATA_DIR + '/perryman/workouts.csv',
            settings.DATA_DIR + '/perryman/plan.csv',
            perryman,
        )
        content = create_salespagecontent("Advanced Lifting", perryman)
        perryman_blitz = Blitz.objects.create(trainer=perryman, workout_plan=perryman_plan,
                                             title="Advanced Lifting", begin_date=datetime.date(2013,6,3))
        perryman_blitz.sales_page_content = content
        perryman_blitz.url_slug = "perryman-advanced"
        perryman_blitz.uses_macros = True
        perryman_blitz.macro_strategy = 'M'
        perryman_blitz.price = 500
        joy_beginner_blitz.recurring = False
        perryman_blitz.save()

        # now set up test users
        ct = create_trainer("CT Fletcher", "ct@example.com", "asdf")
        ct.short_name = "CT"
        ct.save()

        ct.headshot_from_image(settings.TEST_MEDIA_DIR + '/ct.png')

        # sales page for CT
        content = create_salespagecontent("Posting and Toasting", ct)

        blitz = Blitz.objects.create(trainer=ct, workout_plan=roglaw_plan,
            title="Posting and Toasting", begin_date=blitz_start_date, url_slug="CT")
        blitz.sales_page_content = content
        blitz.provisional = True
        blitz.uses_macros = True
        blitz.macro_strategy = 'M'
        blitz.price = 200
        joy_beginner_blitz.recurring = False
        blitz.save()

        carmelo = create_client("Carmelo Anthony", "carmelo@example.com", "asdf", 29, 230, 6, 8, 'M')
        carmelo.headshot_from_image(settings.TEST_MEDIA_DIR + '/carmelo.jpeg')
        add_client_to_blitz(blitz, carmelo)

        amare = create_client("Amar'e Stoudemire", "amare@example.com", "asdf", 31, 245, 6, 11, 'M')
        amare.headshot_from_image(settings.TEST_MEDIA_DIR + '/amare.jpeg')
        add_client_to_blitz(blitz, amare)

        jr = create_client("JR Smith", "jr@example.com", "asdf", 28, 220, 6, 6, 'M')
        jr.headshot_from_image(settings.TEST_MEDIA_DIR + '/jr.jpeg')
        add_client_to_blitz(blitz, jr)

        kidd = create_client("Jason Kidd", "kidd@example.com", "asdf", 28, 210, 6, 4, 'M')
        kidd.headshot_from_image(settings.TEST_MEDIA_DIR + '/kidd.jpeg')
        add_client_to_blitz(blitz, kidd)

        novak = create_client("Steve Novak", "novak@example.com", "asdf", 30, 235, 6, 10, 'M')
        novak.headshot_from_image(settings.TEST_MEDIA_DIR + '/novak.jpeg')
        add_client_to_blitz(blitz, novak)

        content = create_salespagecontent("Posting and Toasting 2", ct)
        blitz2 = Blitz.objects.create(trainer=ct, workout_plan=ct_plan, url_slug="CT2",
            title="Posting and Toasting 2", begin_date=blitz_start_date + datetime.timedelta(weeks=1))
        blitz2.sales_page_content = content
        blitz2.uses_macros = True
        blitz2.macro_strategy = 'M'
        blitz2.price = 199
        blitz2.save()

        aaron = create_client("Aaron Hernandez", "aaron@example.com", "asdf", 29, 230, 6, 8, 'M')
        add_client_to_blitz(blitz2, aaron)

        clients = [carmelo, amare, jr, kidd, novak, aaron]

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
        amarerunning = create_new_parent_comment(amare.user, "Who wants to go for a jog after the gym today?", timezone_now())[0]
        add_like_to_comment(amarerunning, kidd.user, timezone_now())
        add_like_to_comment(amarerunning, jr.user, timezone_now())

        ctcomment = create_new_parent_comment(ct.user, "Hey fellas", timezone_now())[0]

        add_child_to_comment(amarerunning, carmelo.user, "Sure buddy", timezone_now())
        norunning = add_child_to_comment(amarerunning, ct.user,
            "No running! We need you if we are going to win a playoff game!", timezone_now())

        amares_last_session = list(amare.get_gym_sessions())[-1]
        new_content.add_like_to_gym_session(amares_last_session, carmelo.user, timezone_now() )
        new_content.add_comment_to_gym_session(amares_last_session, carmelo.user, "nice glasses", timezone_now() )


        # TODO: parametrize
        body_lifts = ['chinup', 'dips']
        for l in body_lifts:
            lift = Lift.objects.get(slug=l)
            lift.weight_or_body = True
            lift.save()

        # superuser for using admin
        admin = User.objects.create_user('admin', 'admin@example.com', 'admin')
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        #
        # Macros
        #
        macro = MacroDay(client=amare, day=blitz.get_date_for_day_index(3, 0), protein=True, fat=False, carbs=True)
        macro.save()


