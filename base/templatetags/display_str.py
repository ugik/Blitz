from django import template
from django.db.models import get_model
from base.templatetags import units_tags
from django.contrib.auth.models import User

from workouts.models import WorkoutSetCustom
# lazy model import to avoid circular references (when imported from model)
completedset = get_model('base', 'CompletedSet')

register = template.Library()

#Template filters to show completed sets, this was in CompletedSet model but it needs access to non-model variable: the viewer user

@register.filter
def display_str(completedset, viewer):
    Client = get_model('base', 'Client')
    if not viewer or not completedset:
        return ''

    # if viewer is trainer then client will be null
    if viewer.is_trainer:
        client = Client(user=viewer)  # placeholder client object
        client.units = "I"
    else:
        client = viewer.client

    lift = completedset.workout_set.lift

    # intercept for custom workset for client
    custom_set = WorkoutSetCustom.objects.filter(client=client, workoutset=completedset.workout_set).order_by('-pk')
    if custom_set:
        lift = custom_set[0].lift

    if lift.lift_type == 'I':
        if custom_set:
            return "%d secs" % custom_set[0].num_reps
        else:
            return "%d secs" % completedset.num_reps_completed
    elif lift.weight_or_body and not lift.allow_weight_or_body:
        if custom_set:
            return "%d reps" % custom_set[0].num_reps
        else:
            return "%d reps" % completedset.num_reps_completed

    # TODO: body weight weighted
    elif lift.weight_or_body and lift.allow_weight_or_body:
        if completedset.set_type == 'A':
            type_str = '-%.0f' % float(units_tags.lbs_conversion(completedset.weight_in_lbs, client))
        elif completedset.set_type == 'W':
            type_str = '%.0f' % float(units_tags.lbs_conversion(completedset.weight_in_lbs, client))
        else:
            type_str = 'bw'

        return "%d reps (%s)" % (completedset.num_reps_completed, type_str)

    else:
        if completedset.weight_in_lbs:
            weight = float(units_tags.lbs_conversion(completedset.weight_in_lbs, client))
            ds = "%d x %.1f" % (completedset.num_reps_completed, weight)
            # get rid of trailing zeros
            if '.' in ds and ds.endswith('0'):
                ds = ds.rstrip('0').rstrip('.')
            return ds + ' ' + units_tags.weight_label(client.units)
        else:
            return ''


