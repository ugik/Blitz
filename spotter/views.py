from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404, render_to_response, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.views.static import serve
from base.emails import program_loaded, program_assigned
from django.db.models import Q

from base.models import Client, Trainer, Blitz, SalesPageContent, BlitzMember, BlitzInvitation
from workouts.models import WorkoutSet, Lift, Workout, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay, Exercise, ExerciseCustom, WorkoutSet, WorkoutSetCustom
from base.forms import UploadForm
from base.utils import JSONResponse
from spotter.forms import TrainerIDForm, SalesPageForm, AssignPlanForm

import os
import xlrd
import datetime
import requests
from datetime import date, timedelta
from dateutil import rrule

DAYS_OF_WEEK = (
    ('M', 'Monday'),
    ('T', 'Tuesday'),
    ('W', 'Wednesday'),
    ('H', 'Thursday'),
    ('F', 'Friday'),
    ('S', 'Saturday'),
    ('U', 'Sunday'),
)

@login_required
def spotter_index(request):
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'spotter.html')

# review and process outstanding account balances
# option: ?test (shows test users and users with no cc on file)
#         ?trainer= (filters for specific trainer id)
#         ?month= (filters for month #)
#         ?charge (shows only overdue accounts)
#         ?apply (when used w/charge applies charges to overdue accounts)
#
@login_required
def spotter_payments(request):
    import balanced

    trainer = request.GET.get('trainer', None)
    month = request.GET.get('month', None)

    test = True if 'test' in request.GET else None
    charge = True if 'charge' in request.GET else None
    apply = True if 'apply' in request.GET and charge else None

    if trainer:
        trainer = Trainer.objects.get(pk=trainer)

    clients = []
    payments = []
    grand_total_paid = total_cost = total_paid = float(0.0)

    for client in Client.objects.all():
        blitz = client.get_blitz()
        if not blitz:
            continue
        if trainer and trainer != blitz.trainer:
            continue
        # by default ignore test/free users
        if not test and client.balanced_account_uri == '':
            continue

        if client.date_created < blitz.begin_date:
            start_date = blitz.begin_date
        else:
            start_date = client.date_created

        until_date = date.today() if date.today < blitz.end_date else blitz.end_date
        months = (len(list(rrule.rrule(rrule.MONTHLY, start_date, until=until_date))))

        membership = client.blitzmember_set.all()
        if not membership[0].price:   # if there was no special invitation price
            if blitz.price_model == "R":   # recurring price model
                total_cost = months * blitz.price
            else:
                total_cost = blitz.price
        else:
            if blitz.price_model == "R":
                total_cost = months * membership[0].price
            else:
                total_cost = membership[0].price

        debits = balanced.Debit.query.filter(balanced.Debit.f.meta.client_id == client.pk)
        if debits:
            for debit in debits:
                if not month or int(month) == int(debit.created_at[5:7]):
                    if 'client_id' in debit.meta:
                        payments.append({'amount': float(debit.amount)/100, 'status': debit.status, 
                             'created_at': debit.created_at[0:10], 'xtion': debit.transaction_number })
                        total_paid = float(total_paid) + float(debit.amount)/100
                        grand_total_paid += float(debit.amount)/100

        refunds = balanced.Refund.query.filter(balanced.Refund.f.meta.client_id == client.pk)
        if refunds:
            for refund in refunds:
                if not month or int(month) == int(refund.created_at[5:7]):

                    if 'client_id' in debit.meta:
                        payments.append({'amount': float(debit.amount)/-100, 'status': debit.status, 
                             'created_at': debit.created_at[0:10], 'xtion': debit.transaction_number })
                        total_paid = float(total_paid) - float(debit.amount)/100
                        grand_total_paid -= float(debit.amount)/100

        payment = 0
        error = None
        if not charge or float(total_cost)-float(total_paid)>0:

            if apply:   # apply outstanding balance to cc
                card = balanced.Card.fetch(client.balanced_account_uri)
                meta = {"client_id": client.pk, "blitz_id": blitz.pk, 
                        "email": client.user.email}

                try:
                    debit_amount_str = "%d" % (float(total_cost)-float(total_paid))*100
                    #debit = card.debit(appears_on_statement_as = 'Blitz.us payment',
                    #                   amount = debit_amount_str, description='Blitz.us payment', meta=meta)

                    if debit.status != 'succeeded':
                        error = debit.failure_reason

                except Exception as e:
                    error = "Error: %s, %s, %s" % (e.status, e.category_code, e.additional)

                payment = (float(total_cost)-float(total_paid)) if not error else 0

            clients.append({'client':client, 'blitz': blitz, 'membership': membership[0], 'payment': payment,
                            'start':start_date, 'months': months, 'payments': payments, 'error': error,
                            'total_cost': '%.2f' % total_cost, 'total_paid': '%.2f' % total_paid, 'due': '%.2f' % (float(total_cost)-float(total_paid))})

        payments = []
        total_cost = total_paid = 0

    net = float(grand_total_paid * 0.85)
    
    return render(request, 'payments.html', 
          {'clients' : clients, 'test' : test, 'charge' : charge, 'apply' : apply, 'trainer' : trainer, 
           'total' : grand_total_paid, 'net' : net, 'month' : month })

@login_required
def spotter_usage(request):
    from django.utils.timezone import now as timezone_now, get_current_timezone as current_tz
    from pytz import timezone
    from base.tasks import usage_digest
    from django.db.models import Q

    if not request.user.is_staff:
        return redirect('home')

    # get clients with CC on file
    paying_clients = Client.objects.filter(~Q(balanced_account_uri = ''))
    revenue = MRR = 0
    for payer in paying_clients:
        if payer.blitzmember_set:
            # recurring monthly charge
            if not payer.get_blitz().group and payer.blitzmember_set.all()[0].price:
                MRR += float(payer.blitzmember_set.all()[0].price)
            # monthly charge for non-recurring blitz
            else:
                if payer.get_blitz().num_weeks() > 0 and payer.blitzmember_set.all()[0].price:
                    MRR += float(payer.blitzmember_set.all()[0].price / payer.blitzmember_set.all()[0].blitz.num_weeks() * 4)
        revenue += float(payer.blitzmember_set.all()[0].price)

    net = float(MRR * 0.12)
    revenue = float(revenue * 0.12)

    timezone = current_tz()
    if 'days' in request.GET:
        startdate = date.today() - timedelta(days = int(request.GET.get('days')))
        days = request.GET.get('days')
    else:
        days = 1
        startdate = date.today() - timedelta(days = days-1)

    enddate = date.today() - timedelta(days=0)
    trainers = Trainer.objects.filter(date_created__range=[startdate, enddate])
    members = BlitzMember.objects.filter(date_created__range=[startdate, enddate])

    users = User.objects.all()
    login_users = []
    for user in users:
        if timezone.normalize(user.last_login).date() >= startdate:
            login_users.append(user)

    if 'email' in request.GET:
        usage_digest()

    return render(request, 'usage.html', 
          {'days':days, 'trainers':trainers, 'login_users':login_users, 'members':members, 
           'revenue':revenue, 'MRR':MRR, 'net':net })

@login_required
def spotter_delete(request):
    if not request.user.is_staff:
        return redirect('home')

    filename = settings.MEDIA_ROOT + '/documents/'+request.GET.get('file')
    fname = filename[filename.rfind('/')+1:]
    os.renames(filename, filename.replace(fname, 'backup_'+fname))
    return redirect('spotter_uploads')

def spotter_download(request):

    filename = request.GET.get('file')
    if 'dir' in request.GET:
        directory = request.GET.get('dir')
    else:
        directory = '/documents/'

    path = settings.MEDIA_ROOT + directory + filename
    return serve(request, os.path.basename(path), os.path.dirname(path))

@login_required
def spotter_pending_trainers(request):
    if not request.user.is_staff:
        return redirect('home')

    pending_trainers = get_pending_trainers()
    return render(request, 'pending_trainers.html', {'pending' : pending_trainers})

@login_required
def spotter_status_trainers(request):
    if not request.user.is_staff:
        return redirect('home')

    trainers = Trainer.objects.all()
    return render(request, 'trainer_status.html', {'trainers' : trainers, 'errors' : None })


@login_required
# make copy of workoutplan
def copy_workoutplan(request):
    if not request.user.is_staff:
        return redirect('home')

    plan_id = request.GET.get('plan', None)
    workoutplan = WorkoutPlan.objects.get(pk=plan_id)

    if not workoutplan:
        return redirect('home')
    
    wp_copy = WorkoutPlan.objects.create(trainer=workoutplan.trainer, name=workoutplan.name+' (copy)')

    for week in workoutplan.workoutplanweek_set.all():
        week_copy = WorkoutPlanWeek.objects.create(workout_plan=wp_copy, week=week.week)

        for day in week.workoutplanday_set.all():
            slug = "plan%s" % workoutplan.pk
            if slug in day.workout.slug:
                slug_copy = day.workout.slug.replace(slug, "plan%s" % wp_copy.pk)
            else:
                slug_copy = day.workout.slug + "-plan%s" % wp_copy.pk

            workouts = Workout.objects.filter(slug=slug_copy)
            if not workouts:
                workout_copy = Workout.objects.create(display_name=day.workout.display_name, slug=slug_copy)
            else:
                workout_copy = workouts[0]

            day_copy = WorkoutPlanDay.objects.create(workout_plan_week=week_copy, 
                                                     workout=workout_copy,
                                                     day_index=day.day_index,
                                                     day_of_week=day.day_of_week)

            for exercise in day.workout.exercise_set.all():            
                exercise_copy = Exercise.objects.create(lift=exercise.lift, workout=day_copy.workout)
                exercise_copy.sets_display = exercise.sets_display
                exercise_copy.order = exercise.order

                for set in exercise.workoutset_set.all():
                    set_copy = WorkoutSet.objects.create(lift=set.lift, workout=day_copy.workout, exercise=exercise_copy, 
                                                         num_reps=set.num_reps)


    return redirect('spotter_status_trainers')


@login_required
def assign_workoutplan(request):
    if not request.user.is_staff:
        return redirect('home')

    trainers = Trainer.objects.all()

    plan_id = request.GET.get('plan', None)
    workoutplan = WorkoutPlan.objects.get(pk=plan_id)

    blitz_list = []
    blitzes = Blitz.objects.filter(trainer=workoutplan.trainer)
    for blitz in blitzes:
        if blitz.group:
            blitz.title = "Group:"+blitz.title
        if blitz.provisional:
            blitz.title = "Provisional:"+blitz.title
        blitz_list.append(blitz)

    blitz_list.append(Blitz(title='-------------'))

    blitzes = Blitz.objects.filter(~Q(trainer = workoutplan.trainer))
    for blitz in blitzes:
        if blitz.group:
            blitz.title = "Group:"+blitz.title
        if blitz.provisional:
            blitz.title = "Provisional:"+blitz.title
        blitz_list.append(blitz)


    if request.method == 'POST':
        form = AssignPlanForm(request.POST)
        if form.is_valid() and workoutplan:
            blitz_id = form.cleaned_data['blitz_id']

            if blitz_id == 'None':
                response = redirect('spotter_assign_workoutplan')
                return response

            blitz = Blitz.objects.get(pk=blitz_id)
            blitz.workout_plan = workoutplan
            blitz.save()

#            program_assigned(workoutplan, blitz)   # email the trainer

            response = redirect('spotter_status_trainers')
            return response

    form = AssignPlanForm()
    return render(request, 'assign_workoutplan.html', 
           {'form' : form, 'workoutplan' : workoutplan, 'trainers' : trainers, 'blitzes' : blitz_list })

@login_required
def spotter_blitz_sales_pages(request):
    if not request.user.is_staff:
        return redirect('home')

    pending_sales_pages = get_pending_sales_pages()  
    return render(request, 'pending_sales_pages.html', {'pending' : pending_sales_pages})

@login_required
def spotter_lifts(request):
    print "all lifts"
    if not request.user.is_staff:
        return redirect('home')

    lifts = Lift.objects.all() 
    return render(request, 'all_lifts.html', {'lifts' : lifts})

@login_required
def spotter_uploads(request):
    if not request.user.is_staff:
        return redirect('home')

    path = settings.MEDIA_ROOT + '/documents'
    if 'archive' in request.GET:
        doclist = [f[7:] for f in os.listdir(path) if f.startswith('backup_')]
        archive = True
    else:
        doclist = [f for f in os.listdir(path) if not f.startswith('backup_')]
        archive = False

    numdocs = 0
    documents = []

    for doc in doclist:
        user_pk = doc[0:2].strip('_')
        datetime = doc[2:].strip('_').strip('.doc')

        if user_pk.isdigit() and Trainer.objects.filter(pk=user_pk).exists():
            entry = {}
            entry['doc'] = doc
            t = Trainer.objects.get(pk=user_pk)
            # provide template with the date/time sections
            entry['name'] = t.name
            entry['year'] = datetime[0:4]
            entry['month'] = datetime[4:6]
            entry['day'] = datetime[6:8]
            entry['hour'] = datetime[8:10]
            entry['minute'] = datetime[10:12]
            entry['second'] = datetime[12:14]
            documents.append(entry)
            numdocs += 1

    return render(request, 'docs.html', {'docs' : documents, 'numdocs' : numdocs, 'archive' : archive })

@login_required
def spotter_program_upload(request):
    if not request.user.is_staff:
        return redirect('home')

    path = settings.MEDIA_ROOT + '/programs'

    trainers = Trainer.objects.all()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            
            file_name = save_file(request.FILES['document'], path='/programs/', name='prg')

            result = test_program(file_name)

            ready = result['ready']
            log = result['log']
            errors = result['errors']
            form = TrainerIDForm()

            return render_to_response('program_upload_done_page.html', 
                              {'log' : log, 'errors' : errors, 'ready' : ready, 
                               'filename' : file_name, 'form' : form, 'trainers': trainers},
                              RequestContext(request))

        else:
            return render_to_response('program_upload_page.html', 
                               {'form': form, 'trainers': trainers},
                              RequestContext(request))
    else:
        form = UploadForm()

    return render_to_response('program_upload_page.html', 
                              {'form': form, 'trainers': trainers},
                              RequestContext(request))

@login_required
def spotter_program_create(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = TrainerIDForm(request.POST)
        if form.is_valid():
            trainer_id = form.cleaned_data['trainer_id']
            trainer = get_object_or_404(Trainer, id = trainer_id)
            plan_name = form.cleaned_data['program_name']
            file_name = request.GET.get('filename', None)
            result = load_program(file_name, trainer_id, plan_name)

            program_loaded(plan_name, trainer_id)   # email the trainer

            return render_to_response('program_create_done_page.html', 
                              {'plan_name' : plan_name, 'trainer' : trainer},
                              RequestContext(request))
    else:
        form = TrainerIDForm()

    return render_to_response('program_upload_done_page.html', 
                              {'form': form},
                              RequestContext(request))

@login_required
def spotter_workoutplan(request):
    if not request.user.is_staff:
        return redirect('home')

    workoutplan = WorkoutPlan.objects.get(pk=request.GET.get('plan'))
    return render_to_response('workoutplan_page.html', 
                              {'workoutplan' : workoutplan},
                              RequestContext(request))

def flush_session_vars(request):
    for i in range(100):
        if "week_"+str(i) in request.session:
            print "*** del session key:['week_%s']" % i
            del request.session["week_"+str(i)]
        if "day_"+str(i) in request.session:
            print "*** del session key:['day_%s']" % i
            del request.session["day_"+str(i)]
        if "exercise_"+str(i) in request.session:
            print "*** del session key:['exercise_%s']" % i
            del request.session["exercise_"+str(i)]

@login_required
def edit_workoutplan(request):
    if not request.user.is_staff:
        return redirect('home')

    flush_session_vars(request)

    workoutplans = WorkoutPlan.objects.filter(pk=request.GET.get('plan'))
    if workoutplans:
        workoutplan = workoutplans[0]
    else:
        workoutplan = None

    lifts = Lift.objects.all()
    return render_to_response('workoutplan_edit.html', 
                              {'workoutplan' : workoutplan, 'lifts' : lifts},
                              RequestContext(request))
 
@csrf_exempt
def workout_info(request):

    if request.POST.get('slug'):
        workouts = Workout.objects.filter(slug=request.POST.get('slug'))
        if workouts:
            workout = workouts[0]
            if workout:
                return JSONResponse({'num_exercises': len(workout.exercise_set.all()) })

    return JSONResponse({'num_exercises': 0 })

@csrf_exempt
def workoutplan_rename(request):

    if request.POST.get('workoutplan'):
        workoutplan = get_object_or_404(WorkoutPlan, pk = request.POST.get('workoutplan'))

        if workoutplan:
            if request.POST.get('name'):
                workoutplan.name = request.POST.get('name')
                workoutplan.save()
                print "Rename workoutplan pk=%s : %s" % (request.POST.get('workoutplan'), request.POST.get('name'))

    return JSONResponse({})

@csrf_exempt
def workout_desc(request):

    if request.POST.get('workout'):
        workout = get_object_or_404(Workout, pk = request.POST.get('workout'))

        if workout:
            if request.POST.get('desc'):
                workout.description  = request.POST.get('desc')
                workout.save()
                print "Description for workout pk=%s : %s" % (request.POST.get('workout'), request.POST.get('desc'))

    return JSONResponse({})

def new_workoutplan(request):
    flush_session_vars(request)

    trainer = get_object_or_404(Trainer, pk = request.GET.get('trainer'))
    if trainer:
        workoutplan = WorkoutPlan.objects.create(trainer=trainer, name="test")
        workoutplan.name = "%s-%s" % (trainer.short_name, workoutplan.pk)
        workoutplan.save()
    else:
        workoutplan = None

    return redirect('/spotter/edit-workoutplan?plan='+str(workoutplan.pk))

def view_workoutplan(request):
    workoutplans = WorkoutPlan.objects.filter(pk=request.GET.get('plan'))
    if workoutplans:
        workoutplan = workoutplans[0]
    else:
        workoutplan = None

    return render_to_response('workoutplan_view.html', 
                              {'workout_plan' : workoutplan},
                              RequestContext(request))
 

# generate a display for workout
def workout_display(trainer, extra):
#    return "%s %s" % (trainer.short_name, extra)
    return extra

# utility function, manages workoutplanweek/day, returns workoutplanday
def workoutplan_day_mgr(request, workoutplan, key, workout=None, day_char=None):

    wp = WorkoutPlan.objects.get(pk=workoutplan)    # get workoutplan
    week_pk = key.split('_')[0]            # split key into week, day, exercise

    weeks = WorkoutPlanWeek.objects.filter(workout_plan=wp, pk=week_pk)    # get workoutplanweek

    if weeks:
        week = weeks[0]
        print "*** week %s" % weeks[0]
    else:
        session_key = "week_%s" % week_pk
        if session_key not in request.session:
            week = WorkoutPlanWeek.objects.create(workout_plan=wp, week=1)   # this must be first initial week
            request.session[session_key] = week.pk
            print "*** new week key: %s : %s" % (session_key, week.pk)
        else:
            week = WorkoutPlanWeek.objects.get(pk=int(request.session[session_key]))
            print "*** existing week key: %s : %s" % (session_key, week.pk)

    if workout:
        wos = Workout.objects.filter(display_name=workout)    # get workout (the label for the exercises/sets)
        if wos:
            print "*** workout %s" % wos[0]
            workout = wos[0]
        else:
            print "*** new workout %s" % workout
            if workout == '(TBD)':
                display_name = workout_display(wp.trainer, day_char)
                slug = get_slug(wp.trainer.short_name, week.workout_plan.pk, day_char)
            else:
                display_name = workout_display(wp.trainer, workout)
                slug = get_slug(wp.trainer.short_name, week.workout_plan.pk, workout)

            workout = Workout.objects.create(display_name=display_name, slug=slug)

    day_pk = key.split('_')[1]

    days = WorkoutPlanDay.objects.filter(workout_plan_week=week, pk=day_pk)    # get workoutplanday
    if days:
        print "*** day %s" % days[0]
        return days[0]
    else:
        session_key = "day_%s" % day_pk
        if session_key not in request.session:
            day_index = [x for x, y in enumerate(DAYS_OF_WEEK) if y[0] == day_char]
            if day_index:
                day_index = day_index[0]

                day = WorkoutPlanDay.objects.create(workout_plan_week=week, 
                                                     workout=workout,
                                                     day_index=day_index,
                                                     day_of_week=day_char)
                request.session[session_key] = day.pk
                print "*** new day key: %s = %s" % (session_key, day.pk)
            else:
                print "*** invalid day label %s" % day
                day = WorkoutPlanDay()
        else:
            day = WorkoutPlanDay.objects.get(pk=int(request.session[session_key]))
            print "*** existing day key: %s = %s" % (session_key, day.pk)

    return day


@login_required
@csrf_exempt
# multi-purpose ajax function for workoutplan CRUD (create, read, update, delete)
def workoutplan_ajax(request):

    if not 'mode' in request.POST:
        return False

    if request.POST.get('mode') == 'save_day':
        workoutplan_day_mgr(request = request,
                            workoutplan = request.POST.get('workoutplan'),
                            key = request.POST.get('exercise'),
                            workout = request.POST.get('workout'), 
                            day_char = request.POST.get('day'))

    elif request.POST.get('mode') == 'save_exercise':

        week_pk = request.POST.get('exercise').split('_')[0]    # split key into week, day, exercise
        day_pk = request.POST.get('exercise').split('_')[1]
        workoutplan = get_object_or_404(WorkoutPlan, pk=request.POST.get('workoutplan'))
        week = get_object_or_404(WorkoutPlanWeek, pk=week_pk)

        days = WorkoutPlanDay.objects.filter(pk=day_pk)
        if not days or days[0].workout_plan_week.workout_plan != workoutplan:    # check for provisional day
            session_key = "day_%s" % day_pk
            day = WorkoutPlanDay.objects.get(pk=int(request.session[session_key]))            
            print "SAVE EXERCISE REDIRECT WORKOUTDAY:", day_pk, request.session[session_key]
        else:
            day = days[0]

        workout = day.workout

        lifts = Lift.objects.filter(name=request.POST.get('lift'))
        if lifts:
            lift = lifts[0]

            if len(request.POST.get('exercise').split('_'))>2:
                exercise_pk = request.POST.get('exercise').split('_')[2]
                exercises = Exercise.objects.filter(pk=exercise_pk)

                if not exercises or exercises[0].workout != workout:    # check for provisional exercise
                    session_key = "exercise_%s" % exercise_pk
                    if session_key in request.session:
                        exercises = Exercise.objects.filter(pk=int(request.session[session_key]))
                    else:
                        exercises = None

                    if not exercises:    # must be new exercise
                        exercise = Exercise.objects.create(lift=lift, workout=workout)
                        request.session[session_key] = exercise.pk
                        print "SAVE/NEW EXERCISE REDIRECT", request.POST.get('exercise'), exercise.pk
                    else:
                        exercise = exercises[0]
                        exercise.lift = lift
                        print "SAVE/EDIT EXERCISE REDIRECT", request.POST.get('exercise'), exercise.pk
                else:
                    exercise = exercises[0]
                    exercise.lift = lift
                    print "SAVE/EDIT EXERCISE", request.POST.get('exercise')

            else:
                print "NO EXERCISE IN KEY", request.POST.get('exercise')

            exercise.sets_display=request.POST.get('display')
            exercise.save()
            sets = exercise.workoutset_set.all()

            for set_num in range(6):
                if request.POST.get('set'+str(set_num+1)).isdigit():
                    num_reps = int(request.POST.get('set'+str(set_num+1)))
                else:
                    num_reps = 0

                if len(request.POST.get('set'+str(set_num+1)))>0 and len(sets)>set_num:
                    if sets[set_num]:
                        ws = WorkoutSet.objects.get(id=sets[set_num].id)
                        if num_reps>0:
                            ws.num_reps = num_reps
                            ws.save()
                            print "CHANGED SET:", set_num, ws
                        elif ws:
                            ws.delete()
                            print "DELETED SET:", set_num, ws
                elif num_reps>0:
                    ws = WorkoutSet.objects.create(lift=lift, workout=day.workout, exercise=exercise, 
                                                   num_reps=num_reps)
                    print "NEW SET:", ws

            print "SAVE EXERCISE:", request.POST.get('workoutplan'), request.POST.get('exercise'), request.POST.get('lift'), request.POST.get('display'), request.POST.get('set1'), request.POST.get('set2'), request.POST.get('set3'), request.POST.get('set4'), request.POST.get('set5'), request.POST.get('set6')

    elif request.POST.get('mode') == 'delete_workoutplan_day' and request.POST.get('key') != None:

        workoutplan = get_object_or_404(WorkoutPlan, pk=request.POST.get('workoutplan'))

        key = request.POST.get('key')
        if '_' in key:
            day = workoutplan_day_mgr(request = request,
                                      workoutplan = request.POST.get('workoutplan'),
                                      key = key)
        else:
            return JSONResponse({'is_error': True})
        
        workout = day.workout
        week = day.workout_plan_week
        
        # purge leftover records with safechecks to make sure there are no dependencies
        if not day.gymsession_set.all() and not day.traineralert_set.all():
            day.delete()    # delete day IFF it's no longer used
            print "DELETE DAY:", day

        if not workout.exercise_set.all() and not workout.workoutset_set.all() and not workout.workoutplanday_set.all():
            workout.delete()    # delete workout IFF it's no longer used
            print "UNUSED WORKOUT DELETED", workout.slug

        if not week.workoutplanday_set.all():
            week.delete()    # delete week IFF it's no longer used

            for w in WorkoutPlanWeek.objects.filter(workout_plan=workoutplan):
                if w.week >= week.week:
                    w.week -= 1
                    w.save()

            print "UNUSED WEEK DELETED", week
            return JSONResponse({'redirect': '/spotter/edit-workoutplan?plan='+str(workoutplan.pk) })

    elif request.POST.get('mode') == 'delete_workoutplan_exercise':

        if request.POST.get('key') != None:
            week_pk = request.POST.get('key').split('_')[0]    # split key into week, day, exercise
            day_pk = request.POST.get('key').split('_')[1]
            workoutplan = get_object_or_404(WorkoutPlan, pk=request.POST.get('workoutplan'))
            week = get_object_or_404(WorkoutPlanWeek, pk=week_pk)
            days = WorkoutPlanDay.objects.filter(pk=day_pk)
            if not days or days[0].workout_plan_week.workout_plan != workoutplan:    # check for provisional day
                session_key = "day_%s" % day_pk
                day = WorkoutPlanDay.objects.get(pk=int(request.session[session_key]))            
                print "DELETE EXERCISE REDIRECT WORKOUTDAY:", day_pk, request.session[session_key]
            else:
                day = days[0]

            workout = day.workout

            exercise_pk = request.POST.get('key').split('_')[2]

            exercises = Exercise.objects.filter(pk=exercise_pk)

            if not exercises or exercises[0].workout != workout:    # check for provisional exercise
                session_key = "exercise_%s" % exercise_pk
                if session_key in request.session:
                    exercises = Exercise.objects.filter(pk=int(request.session[session_key]))
                    print "DELETE EXERCISE REDIRECT", request.session[session_key], exercise_pk

            if exercises:
                exercise = exercises[0]
                exercise.delete()    # delete exercise and associated workoutsets
                print "DELETE EXERCISE", request.POST.get('key')

    elif request.POST.get('mode') == 'add_week':
        workoutplan = get_object_or_404(WorkoutPlan, pk=request.POST.get('workoutplan'))

        if request.POST.get('exercise')=='999':    # add week to end
            weeks = WorkoutPlanWeek.objects.filter(workout_plan=workoutplan)
            if weeks:
                week = weeks[len(weeks)-1]    # get last week
                print "ADD WEEK after:", week
                WorkoutPlanWeek.objects.create(workout_plan=workoutplan, week=week.week+1)
            else:
                print "ADD WEEK 1"
                WorkoutPlanWeek.objects.create(workout_plan=workoutplan, week=1)

        else:
            week = get_object_or_404(WorkoutPlanWeek, pk=request.POST.get('exercise'))

            for w in WorkoutPlanWeek.objects.filter(workout_plan=workoutplan):
                if w.week >= week.week:
                    w.week += 1
                    w.save()
            WorkoutPlanWeek.objects.create(workout_plan=workoutplan, week=week.week)

            print "ADD WEEK before:", week
        
        return JSONResponse({'redirect': '/spotter/edit-workoutplan?plan='+str(workoutplan.pk) })

    return JSONResponse({'is_error': False})


@login_required
def spotter_feed(request):
    if not request.user.is_staff:
        return redirect('home')

    return render_to_response('feeds.html', {}, RequestContext(request))

@login_required
def spotter_invites(request):
    if not request.user.is_staff:
        return redirect('home')
    
    invites = BlitzInvitation.objects.all()
    return render_to_response('invites.html', { 'invites': invites }, RequestContext(request))

@login_required
def spotter_exercise(request):
    if not request.user.is_staff:
        return redirect('home')

    workout_slug = request.GET.get('workout', None)
    workout = Workout.objects.get(slug=workout_slug)
    workoutset = WorkoutSet.objects.filter(workout_id=workout.id)
    return render_to_response('exercises_page.html', 
                              {'workoutset' : workoutset, 'workout' : workout},
                              RequestContext(request))

@login_required
def spotter_custom_set(request):
    if not request.user.is_staff:
        return redirect('home')

    workoutset_id = request.GET.get('id', None)
    workoutset_custom_id = request.GET.get('custom_id', None)

    if request.method == 'POST':
        if 'client' in request.POST:
            client = Client.objects.get(pk=request.POST['client'])
            if workoutset_custom_id:    # update workoutset custom record
                set = WorkoutSetCustom.objects.get(pk=workoutset_custom_id)
            else:                       # create new workoutset custom record
                set = WorkoutSetCustom()
    #            ws = WorkoutSet.objects.get(pk=workoutset_id)
                set.workoutset_id = workoutset_id
    
            set.lift_id = request.POST['lift']
            set.num_reps = request.POST['num_reps']
            set.client = client
            set.save()

            response = redirect('/spotter/exercise_page')
            response['Location'] += '?workout=%s' % set.workoutset.workout.slug
            return response
        else:
            return redirect('home')
    else:
        if workoutset_custom_id:
        # use custom workoutset if provided
            set = WorkoutSetCustom.objects.get(pk=workoutset_custom_id)
            members = []
            for blitz in set.workoutset.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all():
                members += blitz.blitzmember_set.all()
        else:
            set = WorkoutSet.objects.get(pk=workoutset_id)
            members = []
            for blitz in set.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all():
                members += blitz.blitzmember_set.all()

    
        return render_to_response('custom_set_page.html', 
                  {'workoutset' : set, 
                   'members' : members, 'lifts' : Lift.objects.all()},
                   RequestContext(request))

@login_required
def spotter_custom_exercise(request):
    if not request.user.is_staff:
        return redirect('home')

    exercise_id = request.GET.get('id', None)
    exercise_custom_id = request.GET.get('custom_id', None)
    client = None

    if request.method == 'POST':
        if 'client' in request.POST:
            client = Client.objects.get(pk=request.POST['client'])

            if exercise_custom_id:    # update exercise custom record
                exe = ExerciseCustom.objects.get(pk=exercise_custom_id)
            else:                     # create new exercise custom record
                exe = ExerciseCustom()
                exe.exercise_id = exercise_id

            exe.lift_id = request.POST['lift']
            exe.sets_display = request.POST['sets_display']
            exe.client = client
            exe.save()

            # create commensurate custom sets for lift redundancy in [Exercise, WorkoutSet]
            exercise = exe.exercise
            sets = WorkoutSet.objects.filter(exercise=exercise, workout=exercise.workout)
            for set in sets:
                custom_sets = WorkoutSetCustom.objects.filter(workoutset=set, client=client)
                if not custom_sets:
                    custom_set = WorkoutSetCustom(workoutset=set)
                else:
                    custom_set = custom_sets[0]

                custom_set.num_reps = set.num_reps
                custom_set.client = client
                custom_set.lift = exe.lift
                custom_set.save()

            response = redirect('/spotter/exercise_page')
            response['Location'] += '?workout=%s' % exe.exercise.workout.slug
            return response
        else:
            return redirect('home')

    else:
        if exercise_custom_id:
        # use custom exercise if provided
            exercise = ExerciseCustom.objects.get(pk=exercise_custom_id)
            members = []
            client = exercise.client
            for blitz in exercise.exercise.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all():
                members += blitz.blitzmember_set.all()
        else:
            exercise = Exercise.objects.get(pk=exercise_id)
            members = []
            for blitz in exercise.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all():
                members += blitz.blitzmember_set.all()
    
        return render_to_response('custom_exercise_page.html', 
                  {'exercise' : exercise, 'client' : client, 
                   'members' : members, 'lifts' : Lift.objects.all()},
                   RequestContext(request))


@login_required
def spotter_sales_pages(request):
    if not request.user.is_staff:
        return redirect('home')

    plan_id = request.GET.get('plan', None)

    if request.method == 'POST':
        form = SalesPageForm(request.POST)

        if form.is_valid():
            content = SalesPageContent.objects.get(pk=plan_id)
            update_record = SalesPageForm(request.POST, instance=content)
            update_record.save()
            if request.is_ajax():
                pass
            else:
                return redirect('spotter_blitz_sales_pages')

    else:
        content = SalesPageContent.objects.get(pk=plan_id)
        form = SalesPageForm(instance=content)

    return render_to_response('sales_pages.html', 
                              {'form': form, 'plan': plan_id, 'errors' : form.errors},
                              RequestContext(request))


@login_required
def spotter_sales_pages2(request):

#    import pdb; pdb.set_trace()

    plan_id = request.GET.get('plan', None)

    if request.method == 'POST':
        form = SalesPageForm(request.POST)

        if form.is_valid():
            content = SalesPageContent.objects.get(pk=plan_id)
            update_record = SalesPageForm(request.POST, instance=content)
            update_record.save()
            if request.is_ajax():
                print "Ajax sales page processing..."
            return redirect('spotter_blitz_sales_pages')

    else:
        content = SalesPageContent.objects.get(pk=plan_id)
        form = SalesPageForm(instance=content)

    return render_to_response('sales_pages.html', 
                              {'form': form, 'plan': plan_id, 'errors' : form.errors},
                              RequestContext(request))


@login_required
def spotter_program_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    errors = delete_plan(pk)
    if errors:
        for error in errors:
            print "* %s" % error

    trainers = Trainer.objects.all()
    return redirect('spotter_status_trainers')


def delete_plan(plan_id):

    errors = []
    workoutplan = get_object_or_404(WorkoutPlan, pk=plan_id)
    # can't delete if assigned to Blitz or Invitation
    if workoutplan.blitz_set.all() or workoutplan.blitzinvitation_set.all():
        errors.append("Cannot delete plan %s, in use" % workoutplan.name)
        return errors

    # can't delete if related to old gymsessions
    for workoutplan_week in workoutplan.workoutplanweek_set.all():
        for workoutplan_day in workoutplan_week.workoutplanday_set.all():
            if workoutplan_day.gymsession_set.all():
                errors.append("Cannot delete plan %s, has gym sessions logged on it" % workoutplan.name)
                return errors

    for workout in workoutplan.workouts():    # delete workouts for this workoutplan
         print "DELETE WORKOUT:", workout
         workout.delete()

    print "DELETE WORKOUTPLAN:", workoutplan
    workoutplan.delete()

    return


def get_pending_sales_pages():

    pending_sales_pages = []
    contents = SalesPageContent.objects.all().order_by('-pk')
    for content in contents:
        if content.blitz_set.all():
            pending_sales_pages.append([content.blitz_set.all()[0], 'slug:'+content.blitz_set.all()[0].url_slug, content.name, content.trainer.name])
    return pending_sales_pages


def get_pending_trainers():

    pending_trainers = []
    trainers = Trainer.objects.all()
    for trainer in trainers:
        plan = WorkoutPlan.objects.filter(trainer=trainer.id)
        blitz = Blitz.objects.filter(trainer_id=trainer.id)
        if not plan and not blitz:
        # trainer has no workout plan nor blitz
            pending_trainers.append([trainer.id, trainer.name, 'No WorkoutPlan', 0])
        elif plan and not blitz:
            # trainer has workout plan but no blitz setup
            pending_trainers.append([trainer.id, trainer.name, 'WorkoutPlan but No blitz', plan[0].id])
        elif not plan and blitz:
            # trainer has blitz setup but no plan
            pending_trainers.append([trainer.id, trainer.name, 'Blitz with No WorkoutPlan', 0])
        elif plan and blitz:
            # trainer has blitz and plan
            pending_trainers.append([trainer.id, trainer.name, 'Blitz with WorkoutPlan', -1])

    return pending_trainers


def save_file(file, pk_value=0, name='', path='/documents/'):

#    filename = file._get_name()
    now = datetime.datetime.now()
    if name == '':
        output_file = "%d__%02d%02d%02d%02d%02d%02d.doc" % (pk_value, now.year, now.month, now.day, now.hour, now.minute, now.second)
    else:
        output_file = "%s__%02d%02d%02d%02d%02d%02d.xls" % (name, now.year, now.month, now.day, now.hour, now.minute, now.second)

    file_name = '%s%s%s' % (settings.MEDIA_ROOT, path, output_file)
    fd = open(file_name, 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return file_name


def test_program(file):

    errors = []
    log = []
    days = []
    weekdays = ['M', 'T', 'W', 'H', 'F', 'S', 'U']
    ready = False
    try:
        workbook = xlrd.open_workbook(file)
    except:
        errors.append("MISSING FILE: %s" % file)

    if not errors:
        try:
            worksheet = workbook.sheet_by_name('Meta')
            worksheet = workbook.sheet_by_name('Workouts')
            worksheet = workbook.sheet_by_name('Plan')
        except:
            errors.append("MISSING SHEETS: Need 3 sheets named 'Meta', 'Workouts', 'Plan'")

    if not errors:
        worksheet = workbook.sheet_by_name('Meta')
        try:
            row = worksheet.row(1)

            if len(row)<2:
                errors.append("MISSING DATA: Need 2 columns in Meta sheet")

        except:
            errors.append("MISSING DATA: No rows in Meta sheet")

        try:
            curr_row = 0
            while curr_row < worksheet.nrows - 1:
                curr_row += 1
                try:
                    row = worksheet.row(curr_row)
                    days.append(worksheet.cell_value(curr_row, 0))
                except:
                    errors.append("BAD DATA: Missing days info in Meta tab")

        except:
            errors.append("BAD DATA: Meta tab error")


        log.append("%s rows found in Meta sheet" % str(worksheet.nrows -1))

        worksheet = workbook.sheet_by_name('Workouts')
        try:
            curr_row = 0
            while curr_row < worksheet.nrows - 1:
                curr_row += 1
                row = worksheet.row(curr_row)
                if len(row) < 4:
                    errors.append("MISSING DATA: Need 4 columns in Workout sheet")
                    break
        except:
            errors.append("MISSING DATA: No rows in Workouts sheet")
        try:
            curr_row = 0
            while curr_row < worksheet.nrows - 1:
                curr_row += 1
                try:
                    row = worksheet.row(curr_row)
                    for reps_str in str(worksheet.cell_value(curr_row, 3)).split(','):
                        i = int(float(reps_str))
                    if worksheet.cell_value(curr_row, 0) not in days:
                        errors.append("Workouts day '%s' not defined in Meta tab" % worksheet.cell_value(curr_row, 0))

                except:
                    errors.append("BAD DATA: Workout reps must be comma-separated numbers")
                try:
                    lift = Lift.objects.get(slug=worksheet.cell_value(curr_row, 1))
                except:
                    errors.append("BAD DATA: lift %s not found in Lifts table" % worksheet.cell_value(curr_row, 1))

        except:
            errors.append("BAD DATA: Workout tab error")


        log.append("%s rows found in Workouts sheet" % str(worksheet.nrows -1))

        worksheet = workbook.sheet_by_name('Plan')
        try:
            row = worksheet.row(1)
            if len(row) < 3:
                errors.append("MISSING DATA: Need 3 columns in Plan sheet")
        except:
            errors.append("MISSING DATA: No rows in Plan sheet")
        try:
            curr_row = 0
            while curr_row < worksheet.nrows - 1:
                curr_row += 1
                row = worksheet.row(curr_row)
                i = int(worksheet.cell_value(curr_row, 1))
                if worksheet.cell_value(curr_row, 0) not in days:
                    errors.append("Plan day '%s' not defined in Meta tab" % worksheet.cell_value(curr_row, 0))
                if worksheet.cell_value(curr_row, 2) not in weekdays:
                    errors.append("Plan weekday '%s' invalid" % worksheet.cell_value(curr_row, 2))

        except:
            errors.append("BAD DATA: Plan week must be number")

        log.append("%s rows found in Plan sheet" % str(worksheet.nrows -1))

        if len(errors) == 0:
            ready = True

    return {'errors' : errors, 'log' : log, 'ready' : ready}


# generate slug for workout objects
def get_slug(short_name, plan_pk, exercise):
    return "%s-plan%s-%s" % (short_name, str(plan_pk), exercise)


# load program from 3-sheet XLS file (uploaded by spotter)
def load_program(file, trainer_id, plan_name):

    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_name('Meta')
    # workout meta

    plan = WorkoutPlan.objects.create(name=plan_name, trainer_id=trainer_id)
    trainer = Trainer.objects.get(id=trainer_id)

    curr_row = 0
    while curr_row < worksheet.nrows - 1:
        curr_row += 1
        row = worksheet.row(curr_row)
        slug = get_slug(trainer.short_name, plan.pk, worksheet.cell_value(curr_row, 0))
        workout = Workout.objects.get_or_create(slug=slug, display_name=worksheet.cell_value(curr_row, 1))

    # workout sets
    worksheet = workbook.sheet_by_name('Workouts')
    curr_row = 0
    while curr_row < worksheet.nrows - 1:
        curr_row += 1
        row = worksheet.row(curr_row)

        slug = get_slug(trainer.short_name, plan.pk, worksheet.cell_value(curr_row, 0))
        workout, _ = Workout.objects.get_or_create(slug=slug)
        lift = Lift.objects.get(slug=worksheet.cell_value(curr_row, 1))

        exercise = Exercise.objects.create(lift=lift, 
                                           workout=workout, 
                                           sets_display=worksheet.cell_value(curr_row, 2), 
                                           order=curr_row)

        for reps_str in str(worksheet.cell_value(curr_row, 3)).split(','):
            workout_set = WorkoutSet.objects.create(lift=lift, workout=workout, num_reps=int(float(reps_str)), exercise=exercise)

    # plan schedule
    worksheet = workbook.sheet_by_name('Plan')
    curr_row = 0
    while curr_row < worksheet.nrows - 1:
        curr_row += 1
        row = worksheet.row(curr_row)

    # workout specs
        slug = get_slug(trainer.short_name, plan.pk, worksheet.cell_value(curr_row, 0))
        workout = Workout.objects.get(slug=slug)
        workout_week, _ = WorkoutPlanWeek.objects.get_or_create(workout_plan=plan, 
                          week=int(worksheet.cell_value(curr_row, 1)))

        workout_day, _ = WorkoutPlanDay.objects.get_or_create(workout_plan_week=workout_week,
                         day_of_week=worksheet.cell_value(curr_row, 2),
                         workout=workout)

    return plan

