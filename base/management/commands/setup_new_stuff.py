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

        mikerashid_plan.trainer = mikerashid
        mikerashid_plan.save()

        blitz = Blitz

        try:
            blitz = Blitz.objects.get(url_slug='3weeks')
        except Blitz.DoesNotExist:
            content = create_salespagecontent("3 Week Rashid Plan", mikerashid)
            blitz = Blitz.objects.create(trainer=mikerashid, workout_plan=mikerashid_plan,
                title="3 Week 1:1 Rashid Plan", begin_date=blitz_start_date, url_slug="3weeks")
            blitz.provisional = True
            blitz.recurring = True
            blitz.sales_page_content = content
            blitz.uses_macros = True
            blitz.macro_strategy = 'M'
            blitz.price = 50
            blitz.save()

        invite = BlitzInvitation.objects.create(blitz=blitz, email='vince@example.com', 
                     name='Vince Wilfork', signup_key='TEST1', price=99)

        blitz = Blitz.objects.get(url_slug='3weeks')
        blitz.pk = None
        blitz.provisional = False
        blitz.recurring = True
        blitz.title = "individual:%s blitz:%s" % ("JJ", blitz.url_slug)
        blitz.url_slug = ''
        blitz.begin_date = now.date() - datetime.timedelta(weeks=40)
        blitz.save()

        joe = Client
        try:
            joe = Client.objects.get(name='Joe Johnson')
        except Client.DoesNotExist:
            joe = create_client("Joe Johnson", "joe@example.com", "asdf", 29, 210, 6, 5, 'M')
            joe.headshot_from_image(settings.TEST_MEDIA_DIR + '/jj.jpg')
            add_client_to_blitz(blitz, joe)

        try:
            blitz = Blitz.objects.get(url_slug='mike')
        except Blitz.DoesNotExist:
            content = create_salespagecontent("Mind & Body", mikerashid)
            blitz = Blitz.objects.create(trainer=mikerashid, workout_plan=mikerashid_plan,
                title="Mind & Body Training", begin_date=blitz_start_date, url_slug="mike")
            blitz.provisional = False
            blitz.recurring = False
            blitz.price_model = "O"
            blitz.sales_page_content = content
            blitz.uses_macros = True
            blitz.macro_strategy = 'M'
            blitz.price = 100
            blitz.video_html = "<iframe width='480' height='270' src='//www.youtube.com/embed/uzYoxGY1BmE?feature=player_detailpage' frameborder='0' allowfullscreen></iframe>"
            blitz.save()

        invite = BlitzInvitation.objects.create(blitz=blitz, email='jimmy@example.com', 
                     name='Jimmy McGee', signup_key='TEST2', free=True)

        luke = Client
        try:
            luke = Client.objects.get(name='Luke Walton')
        except Client.DoesNotExist:
            luke = create_client("Luke Walton", "luke@example.com", "asdf", 29, 230, 6, 10, 'M')
            luke.headshot_from_image(settings.TEST_MEDIA_DIR + '/luke_walton.jpg')
            add_client_to_blitz(blitz, luke)
            membership = luke.blitzmember_set.all()[0]   # set membership price to test cc update pay-wall
            membership.price = 99
            membership.save()

        tay = Client
        try:
            tay = Client.objects.get(name='Tayshaun Prince')
        except Client.DoesNotExist:
            tay = create_client("Tayshaun Prince", "tay@example.com", "asdf", 35, 200, 6, 9, 'M')
            tay.headshot_from_image(settings.TEST_MEDIA_DIR + '/tayshaun_prince.png')
            add_client_to_blitz(blitz, tay)

        clients = [luke, tay, joe]

        # seed some demo workout data
        shapeness = knicks_profile()
        for d in clients:
            if d.get_blitz().recurring:
                simulate_recurring_blitz(d.get_blitz(), d, 200, shapeness)
            else:
                simulate_blitz_through_date(d.get_blitz(), d, timezone_now().date(), shapeness)
            d.has_completed_intro = True
            d.save()

        for client in clients:
            for date, day in blitz.iterate_workouts():
                if date >= timezone_now().date(): break
                alerts.create_alerts_for_day(client, date)



        lorem = []
        lorem.append("Vestibulum nec convallis tortor. Etiam ipsum nisl, fermentum a tristique ac, mollis eget arcu. Maecenas malesuada augue arcu, quis aliquam sapien consequat vel. In sit amet bibendum libero. Nunc nec odio facilisis turpis faucibus egestas. Aliquam pulvinar, nulla a suscipit consectetur, tortor metus cursus arcu, in sollicitudin dolor lorem ac magna. Quisque porttitor, dolor in luctus lobortis, magna orci sagittis magna, eu dictum tortor elit in neque. Pellentesque dignissim euismod metus, nec mattis arcu consectetur eget. Pellentesque nec elit sed est suscipit sagittis id sit amet diam. Ut nisl leo, ultricies ut bibendum in, fringilla ac mi.")

        lorem.append("Proin nisi odio, convallis id purus a, venenatis gravida ipsum. Duis molestie orci quis aliquam sagittis. Morbi suscipit massa gravida elit porta suscipit. Donec hendrerit rhoncus mattis. Morbi commodo non enim eget tincidunt. Vestibulum pulvinar magna id ipsum venenatis, in aliquam sem facilisis. Maecenas a libero libero. Vivamus bibendum, leo nec porttitor sagittis, nibh dolor semper mi, eu faucibus odio leo vel tortor. Aliquam sit amet diam sit amet nunc ultricies posuere. Nulla pharetra mi in tincidunt consequat. In sed laoreet sapien. Morbi posuere imperdiet est eget laoreet. Quisque maximus turpis id consectetur posuere. Maecenas ac vehicula velit, vel scelerisque ligula.")

        lorem.append("Curabitur congue mattis rutrum. Suspendisse elit lorem, tristique sed felis quis, sodales accumsan velit. Mauris tellus nibh, posuere eu massa in, pellentesque dictum tellus. Nulla facilisi. Nulla nec enim ultricies, consectetur augue a, pretium odio. Vivamus ex massa, blandit at risus ut, lacinia lacinia est. Aliquam at tellus eu libero finibus feugiat eu et orci. Nulla mattis in nibh et imperdiet. Nam ornare dignissim justo a vehicula. Praesent urna libero, scelerisque sit amet felis eget, scelerisque consectetur nisl.")

        lorem.append("Ut vel nisi metus. Integer porta nulla at mi semper gravida. Integer ipsum nibh, finibus vitae ipsum in, ullamcorper tempor risus. Etiam velit augue, hendrerit ac tortor sit amet, sodales tempor elit. Vestibulum ac nisi erat. Nullam id libero nec lectus hendrerit rhoncus tristique ac sem. Morbi at consequat metus, id ultrices orci. Suspendisse cursus tincidunt odio. Vivamus augue dui, gravida in accumsan sed, ornare quis purus. Aliquam erat volutpat. Aenean a leo mollis, accumsan arcu sit amet, pellentesque nisi. Maecenas laoreet quis arcu sit amet ultricies. In luctus faucibus gravida. Donec tincidunt justo quis eros dapibus finibus non ac mauris.")

        lorem.append("Maecenas vel sem at est viverra pulvinar. Donec sollicitudin tincidunt dui, vel luctus massa. Fusce efficitur rhoncus odio et ultricies. Maecenas convallis, quam in dictum lobortis, ligula velit pulvinar urna, ac tristique turpis lacus id risus. Sed vitae libero vel tellus semper dignissim vitae a nulla. Curabitur diam enim, tincidunt facilisis congue sed, lobortis eu justo. Curabitur aliquam odio ac lorem efficitur malesuada. Suspendisse eu magna nec leo venenatis volutpat non sed enim. Maecenas vestibulum nunc id velit finibus pellentesque. Fusce egestas velit vestibulum ipsum lacinia pulvinar.")

        lorem.append("Donec vel arcu dignissim, varius lacus id, cursus nibh. Nam tincidunt arcu quis faucibus accumsan. Pellentesque id ex et turpis lobortis malesuada id eget risus. Aliquam et posuere massa. Sed imperdiet elit ut viverra vehicula. Phasellus dignissim euismod lectus a consequat. Duis interdum orci quis turpis congue ultrices. Nam in faucibus orci, sit amet pellentesque velit. Pellentesque venenatis metus non purus volutpat, non fringilla massa ultrices. Sed aliquam sem id magna tristique, sed cursus massa ornare. Suspendisse mattis rutrum erat, eget imperdiet enim placerat vitae. Vivamus libero erat, luctus ut tristique ac, porta quis urna. Nunc lacinia justo sed ligula pharetra, eu egestas massa placerat.")

        lorem.append("Duis pretium et tellus et semper. Duis dictum odio in mi maximus luctus. Nulla vitae felis faucibus diam molestie mattis. Etiam sit amet dui nulla. Quisque feugiat massa at erat sagittis, vel euismod nibh tempus. Fusce posuere egestas elementum. Nulla est magna, tincidunt ac ipsum nec, sollicitudin finibus magna. Pellentesque sed tincidunt purus. Integer ut pulvinar nunc. Pellentesque laoreet mauris vel massa aliquet, vel iaculis nisl accumsan. Vivamus ac odio sit amet augue scelerisque malesuada a tincidunt risus. Ut at enim scelerisque, faucibus felis sit amet, fringilla mi.")

        # comments
        lukeburr = create_new_parent_comment(luke.user, "Who wants to go get a burrito?", timezone_now())[0]
        add_like_to_comment(lukeburr, tay.user, timezone_now())

        mrcomment = create_new_parent_comment(mikerashid.user, "Hey boys", timezone_now())[0]

        postdate = date.today() - timedelta(days = randint(50,1500))
        for x in range(0, 1500):   # tons of comments
            mrcomment = create_new_parent_comment(mikerashid.user, lorem[randint(0,6)], postdate)[0]

        add_child_to_comment(lukeburr, luke.user, "Sure buddy", timezone_now())
        noburr = add_child_to_comment(lukeburr, mikerashid.user,
            "No TexMex, get a clue!", timezone_now())

        # Macros
        for x in range(0, 25):
            macro, _ = MacroDay.objects.get_or_create(client=tay, day=blitz.get_date_for_day_index(randint(0,blitz.num_weeks()-1), randint(0,7)))
            protein = True if randint(0,1)==0 else False
            fat = True if randint(0,1)==0 else False
            carbs = True if randint(0,1)==0 else False
            macro.save()
            macro, _ = MacroDay.objects.get_or_create(client=luke, day=blitz.get_date_for_day_index(randint(0,blitz.num_weeks()-1), randint(0,7)))
            protein = True if randint(0,1)==0 else False
            fat = True if randint(0,1)==0 else False
            carbs = True if randint(0,1)==0 else False
            macro.save()
        for x in range(0, 100):   # extra diet entries for JJ over 40-week period
            macro, _ = MacroDay.objects.get_or_create(client=joe, day=blitz.get_date_for_day_index(randint(0,40), randint(0,7)))
            protein = True if randint(0,1)==0 else False
            fat = True if randint(0,1)==0 else False
            carbs = True if randint(0,1)==0 else False
            macro.save()


