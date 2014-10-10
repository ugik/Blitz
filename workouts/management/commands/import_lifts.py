from django.core.management.base import BaseCommand
from workouts.models import Lift
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        lifts_file = open(settings.DATA_DIR + '/lifts.tsv')
        for line in lifts_file:
            if line.strip() == '' or line.startswith('#'): continue
            fields = line.strip('\n').split('\t')
            lift = Lift.objects.get_or_create(slug=fields[0])[0]
            lift.name = fields[1]
            lift.lift_type = fields[2]
            lift.weight_or_body = (True if fields[3] == "1" else False)
            lift.allow_weight_or_body = (True if fields[4] == "1" else False)
            lift.save()
