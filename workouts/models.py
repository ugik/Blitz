from django.db import models
import datetime

DAYS_OF_WEEK = (
    ('M', 'Monday'),
    ('T', 'Tuesday'),
    ('W', 'Wednesday'),
    ('H', 'Thursday'),
    ('F', 'Friday'),
    ('S', 'Saturday'),
    ('U', 'Sunday'),
)

LIFT_TYPES = (
    ('R', 'Reps'),
    ('I', 'Interval'),
)

class Lift(models.Model):
    """
    Lift at the gym - eg Bench Press
    """

    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100, default="")

    # can this be done with weighed / assisted / body weight (eg. chinup)
    weight_or_body = models.BooleanField(default=False)
    allow_weight_or_body = models.BooleanField(default=True)
    lift_type = models.CharField(max_length=1, default="R", choices=LIFT_TYPES)

    def __unicode__(self):
        return self.name


class Workout(models.Model):
    """
    Sum of what you do when you go to the gym
    Includes a set of WorkoutSets
    """

    display_name = models.CharField(max_length=100)

    # Sets are not necessarily grouped by lift - a workout could prescribe bench -> squat -> bench
    # But, usually sets are going to be grouped, so indicate that here
    # Some templates presumably will only render if grouped
    sets_grouped = models.BooleanField(default=True)

    # not for display; only for keeping track of workouts internally
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return "%s (%s)" % (self.display_name, self.slug)

    def get_lifts(self):
        """
        Unique lifts in this workout
        """
        return list(set(ws.lift for ws in self.workoutset_set.all()))

    def get_exercises(self):
        return self.exercise_set.all().order_by('order')


class Exercise(models.Model):
    lift = models.ForeignKey(Lift)
    workout = models.ForeignKey(Workout)
    sets_display = models.CharField(max_length=100, default="")
    order = models.FloatField(default=0.0)

    def num_sets(self):
        return self.workoutset_set.all().count()
       
    def __unicode__(self):
        return "%s of %s in %s" % ( self.sets_display, str(self.lift), str(self.workout) )

# custom exercise record for client
class ExerciseCustom(models.Model):
    client = models.ForeignKey('base.Client')
    exercise = models.ForeignKey(Exercise)

    lift = models.ForeignKey(Lift)
    sets_display = models.CharField(max_length=100, default="")
    date_created = models.DateField(("Date"), default=datetime.date.today)

    def __unicode__(self):
        return "%s of %s in %s (as of %s)" % ( self.sets_display, str(self.lift), str(self.exercise.workout), self.date_created )


class WorkoutSet(models.Model):
    """
    One set in a workout - eg. 10 reps of bench press
    Note that no weight totals here
    """

    lift = models.ForeignKey(Lift) # remove, duplicative
    workout = models.ForeignKey(Workout)
    num_reps = models.IntegerField()
    exercise = models.ForeignKey(Exercise, null=True)

    # order that set should be done; lower comes first
    # if workout.sets_grouped, order is applied *after* grouping
    order = models.FloatField(default=0.0)

    def __unicode__(self):
        return "%d reps of %s in %s" % ( self.num_reps, str(self.lift), str(self.workout) )

# custom workoutset record for client
class WorkoutSetCustom(models.Model):
    client = models.ForeignKey('base.Client')
    workoutset = models.ForeignKey(WorkoutSet)

    lift = models.ForeignKey(Lift)
    num_reps = models.IntegerField()
    date_created = models.DateField(("Date"), default=datetime.date.today)

    def __unicode__(self):
        return "%d reps of %s in %s" % ( self.num_reps, str(self.lift), str(self.workoutset.workout) )


class WorkoutPlan(models.Model):
    """
    A full workout plan (program)
    """

    name = models.CharField(max_length=100, default="")

    trainer = models.ForeignKey('base.Trainer', null=True)

    def __unicode__(self):
        if self.trainer:
            return "%s (pk:%d) trainer:%s" % (self.name, self.pk, self.trainer.name)
        else:
            return "%s (pk:%d)" % (self.name, self.pk)

    def num_weeks(self):
        return self.workoutplanweek_set.count()

    def iterate_days(self):
        """
        generator of workoutplandays in order
        """
        for workout_plan_week in self.workoutplanweek_set.all().order_by('week'):
            for workout_plan_day in workout_plan_week.workoutplanday_set.all().order_by('day_index'):
                yield workout_plan_day

    def all_lifts(self):
        return list(set([d.workout.get_lifts()[0] for d in self.iterate_days()]))

    def weeks(self):
        return self.workoutplanweek_set.all().order_by('week')


class WorkoutPlanWeek(models.Model):
    """
    One week in a plan
    Contains a set of workout days with meta info, sometimes content like an article of the week
    *** WEEKS ARE ALWAYS 1-INDEXED ***
    """

    workout_plan = models.ForeignKey(WorkoutPlan)

    # *** WEEKS ARE ALWAYS 1-INDEXED ***
    week = models.IntegerField()

    def __unicode__(self):
        return "Week %d of %s" % ( self.week, str(self.workout_plan) )

    def days(self):
        return self.workoutplanday_set.all().order_by('day_index')

class WorkoutPlanDay(models.Model):
    """
    Workout embedded in a day of a plan
    """

    workout_plan_week = models.ForeignKey(WorkoutPlanWeek)
    day_of_week = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    day_index = models.IntegerField(default=-1)
    workout = models.ForeignKey(Workout)

    def __unicode__(self):
        return "%s of week %s in plan %s" % (
            self.day_of_week,
            str(self.workout_plan_week),
            str(self.get_workout_plan())
        )

    def get_workout_plan(self):
        return self.workout_plan_week.workout_plan

    def get_week(self):
        return self.workout_plan_week.week

    def get_day_name(self):
        return DAYS_OF_WEEK[self.day_index][1]

    def save(self, *args, **kwargs):
        self.day_index = next(i for i, d in enumerate(DAYS_OF_WEEK) if d[0] == self.day_of_week)
        super(WorkoutPlanDay, self).save(*args, **kwargs)

