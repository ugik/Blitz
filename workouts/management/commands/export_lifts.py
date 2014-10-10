from django.core.management.base import BaseCommand
from optparse import make_option
from workouts.models import Lift

class Command(BaseCommand):

    def handle(self, *args, **options):
        headers = [
            "#SLUG",
            "NAME",
            "REPS_OR_INTERVAL",
            "BODY_WEIGHT",
            "ALLOW_ASSISTED_AND_WEIGHTED"
        ]
        print "\t".join(headers)
        for lift in Lift.objects.all():
            fields = [
                lift.slug,
                lift.name,
                lift.lift_type,
                "1" if lift.weight_or_body else "0",
                "1" if lift.allow_weight_or_body else "0",
            ]
            print "\t".join(fields)