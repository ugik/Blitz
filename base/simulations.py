from base.models import GymSession, CompletedSet
from base.new_content import finalize_gym_session
from workouts.utils import get_grouped_sets

import pytz
import random
from random import randint
import datetime
from datetime import date, timedelta
from dateutil import rrule
from django.utils.timezone import now as timezone_now

P_COMPLETED_WORKOUT = .5 # probability that a user actually did a given gym session
P_COMPLETED_SET = .8 # prob that a user completed a set (given that they went to the gym)

class Shapeness(object):

    def __init__(self):
        self._tenRepMaxes = {}

    def setTenRepMax(self, lift_slug, weight):
        self._tenRepMaxes[lift_slug] = weight

    def tenRepMax(self, lift_slug):
        return self._tenRepMaxes[lift_slug]

def knicks_profile():

    fp = Shapeness()
    fp.setTenRepMax('back-squat', 101)
    fp.setTenRepMax('overhead-press', 102)
    fp.setTenRepMax('bench-press', 103)
    fp.setTenRepMax('push-press', 104)
    fp.setTenRepMax('incline-bench-press', 105)
    fp.setTenRepMax('high-pull', 106)
    fp.setTenRepMax('pendlay-row', 107)
    fp.setTenRepMax('front-squat', 108)
    fp.setTenRepMax('deadlift', 109)
    fp.setTenRepMax('curl', 110)
    fp.setTenRepMax('tricep-extension', 111)
    fp.setTenRepMax('back-extension', 112)
    fp.setTenRepMax('chinup', 110)

    return fp

def simulate_gym_session(client, date, workout_plan_day, shapeness):

    gym_session = GymSession.objects.create(date_of_session=date,
        workout_plan_day=workout_plan_day, client=client)

    for group in get_grouped_sets(workout_plan_day.workout):
        for workoutset in group['sets']:
            if random.random() > P_COMPLETED_SET: continue
            #weight = shapeness.tenRepMax(group['lift'].slug) * random.uniform(0.5, 1.5)
            weight = 100 * random.uniform(0.5, 1.5)
            weight = round(weight, 0)
            if random.random() > .8: weight += .5
            CompletedSet.objects.create(gym_session=gym_session, workout_set=workoutset, num_reps_completed=8,
                weight_in_lbs=weight)

    return gym_session

def simulate_blitz_through_date(blitz, client, to_date, shapeness):
    """
    Simulate blitz data up through (inclusive) week and day
    """
    for date, workout_plan_day in blitz.iterate_workouts():

        if date > to_date: break

        # did user skip?
        if random.random() > P_COMPLETED_WORKOUT: continue

        gym_session = simulate_gym_session(client, date, workout_plan_day, shapeness)
        finalize_gym_session(blitz, gym_session, pytz.timezone('UTC').localize(datetime.datetime.combine(gym_session.date_of_session, datetime.time() )) )

def simulate_recurring_blitz(blitz, client, num_workouts, shapeness):
    """
    Simulate blitz data up through (inclusive) week and day for recurring blitz
    """
    for i in range(1, num_workouts):
        back = randint(1,300)    # random # of days
        date = date.today() - timedelta(days = back)

        # did user skip?
        if random.random() > P_COMPLETED_WORKOUT: continue

        gym_session = simulate_gym_session(client, date, workout_plan_day, shapeness)
        finalize_gym_session(blitz, gym_session, pytz.timezone('UTC').localize(datetime.datetime.combine(gym_session.date_of_session, datetime.time() )) )


