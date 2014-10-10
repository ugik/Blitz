from django.contrib import admin
from workouts.models import Lift, Workout, WorkoutSet, WorkoutPlan, WorkoutPlanWeek, WorkoutPlanDay, Exercise

admin.site.register(Workout)
admin.site.register(WorkoutSet)
admin.site.register(WorkoutPlan)
admin.site.register(WorkoutPlanWeek)
admin.site.register(WorkoutPlanDay)
admin.site.register(Lift)
admin.site.register(Exercise)