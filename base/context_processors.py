from django.contrib.sites.models import Site
from django.conf import settings

def custom_processor(request):

    return {
        'CURRENT_URL':  Site.objects.get_current().domain,
    }