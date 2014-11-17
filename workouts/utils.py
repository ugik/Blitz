from workouts.models import WorkoutSet, Lift, Workout, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay, Exercise, ExerciseCustom, WorkoutSetCustom
from workouts.templatetags import custom_exercise

from django.conf import settings

import csv

def load_workout_plan_from_fileset(plan_name, workout_meta_file, workouts_file, plan_file):
    workout_meta_file = open(workout_meta_file, 'rU')
    for row in csv.reader(workout_meta_file):
        workout = Workout.objects.get_or_create(slug=row[0], display_name=row[1])

    workouts_file = open(workouts_file, 'rU')
    for row in csv.reader(workouts_file):
        lift = Lift.objects.get(slug=row[1].lower())
        workout, _ = Workout.objects.get_or_create(slug=row[0])
        workout_set = WorkoutSet.objects.create(lift=lift, workout=workout, num_reps=row[2])

    # load perryman plan day data
    perryman_plan = WorkoutPlan(name=plan_name)
    perryman_plan.save()

    plan_file = open( plan_file, 'rU')
    for row in csv.reader(plan_file):
        workout = Workout.objects.get(slug=row[0])
        workout_plan_week, _ = WorkoutPlanWeek.objects.get_or_create(workout_plan=perryman_plan, week=int(row[1]))
        workout_plan_day, _ = WorkoutPlanDay.objects.get_or_create(
            workout_plan_week=workout_plan_week,
            day_of_week=row[2],
            workout=workout
        )
    return perryman_plan

def load_workout_from_file(workout, f):
    """
    Load a workout from text file; f is file-like
    """

    for i, _line in enumerate(f):
        line = _line.strip()
        lift_slug, num_reps = line.split()
        lift = Lift.objects.get(slug=lift_slug)
        ws = WorkoutSet( workout=workout, lift=lift, num_reps=int(num_reps) )
        ws.save()

def get_set_group_title(set_group):
    """
    Display these sets for humans
    Example "3 sets of 12 reps"
    """
    reps = [s.num_reps for s in set_group]
    if len(set(reps)) == 1:
        return "%d sets of %d reps" % ( len(reps), reps[0] )
    raise Exception("Cannot display this set group")

# todo: this is pathetic, do a real groupby
# todo: also return tuple not dict
def get_grouped_sets(workout, client=None, gym_date=None):
    """
    Gets a list of "grouped sets" from a workout. Each item is:
    {
        'lift':
        'sets':
        'title':
    }
    """
    groups = []
    for exercise in workout.get_exercises():
        sets = exercise.workoutset_set.all()

        # Custom exercise intercept
        custom = ExerciseCustom.objects.filter(client=client, exercise=exercise).order_by('-pk')
        if custom:
            if custom[0].date_created <= gym_date:
                exercise.lift = custom[0].lift
                exercise.sets_display = custom[0].sets_display
                for i,set in enumerate(sets):
                    c_set = WorkoutSetCustom.objects.filter(client=client, workoutset=set).order_by('-pk')
                    if c_set and c_set[0].date_created <= gym_date:
                        if c_set:
                            sets[i].lift = c_set[0].lift
                            sets[i].num_reps = c_set[0].num_reps

#        import pdb; pdb.set_trace()

        groups.append({
            'exercise': exercise,
            'lift': custom_exercise.custom_lift(exercise, client, gym_date),
            'sets': sets,
            'title': custom_exercise.custom_sets_display(exercise, client, gym_date),
        })
    return groups


def load_workout_plan_from_fileset_2(plan_name, workout_meta_file, workouts_file, plan_file, trainer=None):

    # workout meta
    for line in open(workout_meta_file):
        if line.strip() == '' or line.startswith('#'): continue
        fields = line.strip('\n').split('\t')
        workout = Workout.objects.get_or_create(slug=fields[0], display_name=fields[1])

    # workout sets
    for i, line in enumerate(open(workouts_file)):
        if line.strip() == '' or line.startswith('#'): continue
        fields = line.strip('\n').split('\t')

        workout, _ = Workout.objects.get_or_create(slug=fields[0])
        lift = Lift.objects.get(slug=fields[1].lower())

        exercise = Exercise.objects.create(lift=lift, workout=workout, sets_display=fields[2], order=i)
        for reps_str in fields[3].split(','):
            workout_set = WorkoutSet.objects.create(lift=lift, workout=workout, num_reps=int(reps_str), exercise=exercise)

    # plan schedule
    plan = WorkoutPlan.objects.create(name=plan_name, trainer=trainer)

    # workout specs
    for line in open(plan_file):
        if line.strip() == '' or line.startswith('#'): continue
        fields = line.strip('\n').split('\t')

        workout = Workout.objects.get(slug=fields[0])
        workout_plan_week, _ = WorkoutPlanWeek.objects.get_or_create(workout_plan=plan, week=int(fields[1]))

        workout_plan_day, _ = WorkoutPlanDay.objects.get_or_create(
            workout_plan_week=workout_plan_week,
            day_of_week=fields[2],
            workout=workout
        )

    return plan

