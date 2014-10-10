from base.utils import JSONResponse
from base.models import MacroDay
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from base import macro_utils

@login_required
@csrf_exempt
def get_macros_for_blitz_week(request):
    """
    List of macros for a given week
    """
    week = int(request.GET['week'])
    elements = []
    for i in range(7):
        elements.append(macro_utils.get_macro_meta_for_day(request.user.client, week, i))
    ret = {
        'week_macros': elements,
    }
    return JSONResponse(ret)

def set_macros_for_blitz_day(request):
    """
    Submit macros for a given day
    """
    pass

@login_required
@csrf_exempt
def undo_macro_day(request):
    week = int(request.POST.get('week'))
    day_index = int(request.POST.get('day_index'))
    client = request.user.client
    blitz = request.user.blitz
    date = blitz.get_date_for_day_index(week, day_index)
    md = MacroDay.objects.get(client=client, day=date)
    md.delete()
    return JSONResponse(macro_utils.get_macro_meta_for_day(client, week, day_index))

@login_required
@csrf_exempt
def save_macro_day(request):
    week = int(request.POST.get('week'))
    day_index = int(request.POST.get('day_index'))
    client = request.user.client
    blitz = request.user.blitz
    date = blitz.get_date_for_day_index(week, day_index)

    # TODO better error handling, need client's cooperation tho
    if not MacroDay.objects.filter(client=client, day=date).exists():
        md = MacroDay.objects.create(
            client=client,
            day=date,
            calories=request.POST.get('calories') == 'yes',
            carbs=request.POST.get('carbs') == 'yes',
            protein=request.POST.get('protein') == 'yes',
            fat=request.POST.get('fat') == 'yes',
        )

    return JSONResponse(macro_utils.get_macro_meta_for_day(client, week, day_index))