from base.models import MacroDay, Blitz

def get_macro_targets_for_day(client, week, day):
    """
    Macro targets for a given day
    Return dict with following structure:
    {
        'protein': {'min': 100, 'max': 120 },
        ...
    }
    """
    return {
        'protein': {'min': 100, 'max': 110 },
        'carbs': {'min': 110, 'max': 120 },
        'fat': {'min': 120, 'max': 130 },
    }

def get_macro_meta_for_day(client, week, day_index):
    date = client.get_blitz().get_date_for_day_index(week, day_index)
    if MacroDay.objects.filter(day=date, client=client).exists():
        md = MacroDay.objects.get(day=date, client=client)
        d = md.toJSON()
        d['has_entry'] = True
    else:
        d = {}
        d['has_entry'] = False

    d['day_str'] = date.strftime("%A") + ' %d/%d' % (date.month, date.day)
    d['week'] = week
    d['day_index'] = day_index
    d['targets'] = client.macro_target_for_date(date)
    d['day_of_month'] = date.day
    d['in_future'] = date > client.current_datetime().date()
    return d

def get_macros_for_blitz_week(client, week):
    """
    List with 7 items; ordered list of MacroDays for a given week
    Item is None if none for that day
    """
    ret = []
    for i in range(7):
        date = client.get_blitz().get_date_for_day_index(week, i)
        md = MacroDay.objects.filter(day=date, client=client)
        if md.exists():
            ret.append(md[0])
        else:
            ret.append(None)
    return ret

def get_full_macro_history(client):
    blitz = client.get_blitz()
    weeks = []
    for i in range(1, blitz.num_weeks()+1):
        one_week = {
            'week_number': i,
            'macro_days': []
        }
        for j in range(7):
            one_week['macro_days'].append(get_macro_meta_for_day(client, i, j))
        weeks.append(one_week)
    return weeks
