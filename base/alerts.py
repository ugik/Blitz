from base.models import Client, Trainer, TrainerAlert
from django.utils.timezone import now as timezone_now

def create_alerts_for_day(client, day):

    # missed a workout on this day
    if client.get_blitz().workout_plan:
        day_workout = client.get_blitz().get_workout_for_date(day)
        if day_workout and not client.gymsession_set.filter(workout_plan_day=day_workout).exists():
            alert = TrainerAlert.objects.create(
                alert_type="W",
                trainer=client.get_blitz().trainer,
                client=client,
                date_created=day,
                workout_plan_day=day_workout
            )

