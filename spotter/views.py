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

from base.models import Client, Trainer, Blitz, SalesPageContent, BlitzMember
from workouts.models import WorkoutSet, Lift, Workout, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay, Exercise, ExerciseCustom, WorkoutSet, WorkoutSetCustom
from base.forms import UploadForm
from spotter.forms import TrainerIDForm, SalesPageForm, AssignPlanForm

import os
import xlrd
import datetime
import requests
from datetime import date, timedelta
#    import pdb; pdb.set_trace()

@login_required
def spotter_index(request):
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'spotter.html')

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
    MRR = 0
    for payer in paying_clients:
        if payer.blitzmember_set:
            # recurring monthly charge
            if payer.blitzmember_set.all()[0].blitz.recurring:
                MRR += float(payer.blitzmember_set.all()[0].blitz.price)
            # monthly charge for non-recurring blitz
            else: 
                MRR += float(payer.blitzmember_set.all()[0].blitz.price / payer.blitzmember_set.all()[0].blitz.num_weeks() * 4)

    timezone = current_tz()
    if 'days' in request.GET:
        startdate = date.today() - timedelta(days = int(request.GET.get('days')))
        days = request.GET.get('days')
    else:
        days = 3
        startdate = date.today() - timedelta(days = days)

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
          {'days':days, 'trainers':trainers, 'login_users':login_users, 'members':members, 'MRR':MRR})

@login_required
def spotter_delete(request):
    if not request.user.is_staff:
        return redirect('home')

    filename = settings.MEDIA_ROOT + '/documents/'+request.GET.get('file')
    os.renames(filename, filename+'.backup')
    return redirect('spotter_uploads')

@login_required
def spotter_download(request):
    if not request.user.is_staff:
        return redirect('home')

    filename = request.GET.get('file')
    directory = request.GET.get('dir')
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
    return render(request, 'trainer_status.html', {'trainers' : trainers })

@login_required
def assign_workoutplan(request):
    if not request.user.is_staff:
        return redirect('home')

    trainers = Trainer.objects.all()
    blitzes = Blitz.objects.all()
    plan_id = request.GET.get('plan', None)
    workoutplan = WorkoutPlan.objects.get(pk=plan_id)

    if request.method == 'POST':
        form = AssignPlanForm(request.POST)
        if form.is_valid() and workoutplan:
            blitz_id = form.cleaned_data['blitz_id']
            blitz = Blitz.objects.get(pk=blitz_id)
            blitz.workout_plan = workoutplan
            blitz.save()
            response = redirect('spotter_status_trainers')
            return response

    form = AssignPlanForm()
    return render(request, 'assign_workoutplan.html', 
           {'form' : form, 'workoutplan' : workoutplan, 'trainers' : trainers, 'blitzes' : blitzes })

@login_required
def spotter_blitz_sales_pages(request):
    if not request.user.is_staff:
        return redirect('home')

    pending_sales_pages = get_pending_sales_pages()        
    return render(request, 'pending_sales_pages.html', {'pending' : pending_sales_pages})

@login_required
def spotter_uploads(request):
    if not request.user.is_staff:
        return redirect('home')

    path = settings.MEDIA_ROOT + '/documents'
    doclist = [f for f in os.listdir(path) if not f.endswith('.backup')]
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

    return render(request, 'docs.html', {'docs' : documents, 'numdocs' : numdocs})

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
            plan_name = form.cleaned_data['program_name']
            file_name = request.GET.get('filename', None)
            result = load_program(file_name, trainer_id, plan_name)

            return render_to_response('program_create_done_page.html', 
                              {'plan_name' : plan_name, 'trainer_id' : trainer_id},
                              RequestContext(request))
    else:
        form = TrainerIDForm()

    return render_to_response('program_upload_done_page.html', 
                              {'form': form},
                              RequestContext(request))

@login_required
def spotter_workouts(request):
    if not request.user.is_staff:
        return redirect('home')

    workouts = Workout.objects.all()
    return render_to_response('workouts_page.html', 
                              {'workouts' : workouts},
                              RequestContext(request))

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
#        import pdb; pdb.set_trace()
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
        if workoutset_custom_id:
        # use custom workoutset if provided
            set = WorkoutSetCustom.objects.get(pk=workoutset_custom_id)
            members = set.workoutset.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all()[0].blitzmember_set.all()
        else:
            set = WorkoutSet.objects.get(pk=workoutset_id)
            members = set.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all()[0].blitzmember_set.all()
    
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

    if request.method == 'POST':
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

        response = redirect('/spotter/exercise_page')
        response['Location'] += '?workout=%s' % exe.exercise.workout.slug
        return response

    else:
        if exercise_custom_id:
        # use custom exercise if provided
            exercise = ExerciseCustom.objects.get(pk=exercise_custom_id)
            members = exercise.exercise.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all()[0].blitzmember_set.all()
        else:
            exercise = Exercise.objects.get(pk=exercise_id)
            members = exercise.workout.workoutplanday_set.all()[0].workout_plan_week.workout_plan.blitz_set.all()[0].blitzmember_set.all()
    
        return render_to_response('custom_exercise_page.html', 
                  {'exercise' : exercise,
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
            return render_to_response('sales_pages.html', 
                              {'form': form, 'errors' : form.errors},
                              RequestContext(request))
    else:
        content = SalesPageContent.objects.get(pk=plan_id)
        form = SalesPageForm(instance=content)

    return render_to_response('sales_pages.html', 
                              {'form': form, 'errors' : form.errors},
                              RequestContext(request))


@login_required
def spotter_program_delete(request):
    if not request.user.is_staff:
        return redirect('home')

    plan_id = request.GET.get('plan', None)
    errors = delete_plan(plan_id)
    pending_trainers = get_pending_trainers()
    if request.user.is_superuser:
        return render(request, 'pending_trainers.html', 
                {'pending' : pending_trainers, 'errors' : errors})
    else:    
        return render(request, 'pending_trainers.html', 
                {'pending' : pending_trainers, 'errors' : errors})



def delete_plan(plan_id):

    errors = []
    plan = WorkoutPlan.objects.filter(id=plan_id)
    if plan:
        weeks = WorkoutPlanWeek.objects.filter(workout_plan_id=plan[0].id)
        for week in weeks:
            days = WorkoutPlanDay.objects.filter(workout_plan_week_id=week.id)
            for day in days:
                exercises = Exercise.objects.filter(workout_id=day.workout.id)
                for exercise in exercises:
                    exercise.delete()
                day.delete()
                day.workout.delete()
            week.delete()
        plan.delete()
    else:
        errors.append('No plan with id#%s' % plan_id)

    return errors


def get_pending_sales_pages():

    pending_sales_pages = []
    contents = SalesPageContent.objects.all()
    for content in contents:
        pending_sales_pages.append([content.id, content.name, content.trainer.name, content.program_title])
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
                    for reps_str in worksheet.cell_value(curr_row, 3).split(','):
                        i = int(reps_str)
                except:
                    errors.append("BAD DATA: Workout reps must be comma-separated numbers")
                try:
                    lift = Lift.objects.get(slug=worksheet.cell_value(curr_row, 1).lower())
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
        except:
            errors.append("BAD DATA: Plan week must be number")

        log.append("%s rows found in Plan sheet" % str(worksheet.nrows -1))

        if len(errors) == 0:
            ready = True

#    import pdb; pdb.set_trace()
    return {'errors' : errors, 'log' : log, 'ready' : ready}


def load_program(file, trainer_id, plan_name):

    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_name('Meta')
    # workout meta
    curr_row = 0
    while curr_row < worksheet.nrows - 1:
        curr_row += 1
        row = worksheet.row(curr_row)
        workout = Workout.objects.get_or_create(
                     slug="%s_%s" % (str(trainer_id), worksheet.cell_value(curr_row, 0)),
                     display_name=worksheet.cell_value(curr_row, 1))
    
    # workout sets
    worksheet = workbook.sheet_by_name('Workouts')
    curr_row = 0
    while curr_row < worksheet.nrows - 1:
        curr_row += 1
        row = worksheet.row(curr_row)

        workout, _ = Workout.objects.get_or_create(
                      slug="%s_%s" % (str(trainer_id), worksheet.cell_value(curr_row, 0)))
        lift = Lift.objects.get(slug=worksheet.cell_value(curr_row, 1).lower())

        exercise = Exercise.objects.create(lift=lift, 
                                           workout=workout, 
                                           sets_display=worksheet.cell_value(curr_row, 2), 
                                           order=curr_row)

        for reps_str in worksheet.cell_value(curr_row, 3).split(','):
            workout_set = WorkoutSet.objects.create(lift=lift, workout=workout, num_reps=int(reps_str), exercise=exercise)

    # plan schedule
    plan = WorkoutPlan.objects.create(name=plan_name, trainer_id=trainer_id)

    worksheet = workbook.sheet_by_name('Plan')
    curr_row = 0
    while curr_row < worksheet.nrows - 1:
        curr_row += 1
        row = worksheet.row(curr_row)

    # workout specs
        workout = Workout.objects.get(
                      slug="%s_%s" % (str(trainer_id), worksheet.cell_value(curr_row, 0)))
        workout_week, _ = WorkoutPlanWeek.objects.get_or_create(workout_plan=plan, 
                          week=int(worksheet.cell_value(curr_row, 1)))

        workout_day, _ = WorkoutPlanDay.objects.get_or_create(workout_plan_week=workout_week,
                         day_of_week=worksheet.cell_value(curr_row, 2),
                         workout=workout)

    return plan

