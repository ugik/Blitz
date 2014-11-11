from django import template
from workouts.models import Exercise, ExerciseCustom, WorkoutSetCustom
from base.models import Client, GymSession
from django.contrib.auth.models import User
from django.http import QueryDict

register = template.Library()

#Template filters to show custom exercise sets_display and exercise lift

@register.filter
def display_lift(value, args):
    qs = QueryDict(args)

    client = Client.objects.get(pk=qs['c'])
    if not client:
        return value.lift
    gym_session = GymSession.objects.get(pk=qs['g'])
    if not gym_session:
        return value.lift

    custom = ExerciseCustom.objects.filter(client=client, exercise=value).order_by('-pk')
    if custom:
        if gym_session and custom[0].date_created <= gym_session.date_of_session:
            return custom[0].lift
    return value.lift

@register.filter
def custom_lift(value, client, gym_date=None):
    if not client:
        return value.lift

    custom = ExerciseCustom.objects.filter(client=client, exercise=value).order_by('-pk')
    if custom:
        if gym_date and custom[0].date_created <= gym_date:
            return custom[0].lift
    return value.lift

@register.filter
def custom_sets_display(value, client, gym_date=None):
    if not client: 
        return value.sets_display
    custom = ExerciseCustom.objects.filter(client=client, exercise=value).order_by('-pk')
    if custom:
        if gym_date and custom[0].date_created <= gym_date:
            return custom[0].sets_display
    return value.sets_display

@register.filter
def custom_workout_lifts(value, client):
    workout = value
    lifts = list(set(ws.lift for ws in workout.workoutset_set.all()))    
    for workoutset in workout.workoutset_set.all():
        if workoutset.lift in lifts:
            lifts.remove(workoutset.lift)
        custom = custom_workoutset_lift(workoutset, client)  # get the custom lift if applicable
        if custom not in lifts:
            lifts.append(custom)
    return lifts

@register.filter
def custom_workoutset(value, client):
    if not client:
        return value
    custom = WorkoutSetCustom.objects.filter(client=client, workoutset=value).order_by('-pk')
    if custom:
        return custom[0]
    else:
        return value

@register.filter
def custom_workoutset_lift(value, client):
    if not client:
        return value.lift
    custom = WorkoutSetCustom.objects.filter(client=client, workoutset=value).order_by('-pk')
    if custom:
        return custom[0].lift
    else:
        return value.lift

@register.filter
def custom_workoutset_num_reps(value, client):
    if not client:
        return value.num_reps

    custom = WorkoutSetCustom.objects.filter(client=client, workoutset=value).order_by('-pk')
    if custom:
        return custom[0].num_reps
    else:
        return value.num_reps

