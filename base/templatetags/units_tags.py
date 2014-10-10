from django import template

register = template.Library()

#Template filters to show measurements in selected units

@register.filter
def lbs_conversion(value, client):
# converts lbs to kg according to client.units setting
    if value:
        RATIO = 0.45359237
        if client.units == "M":
            return "{:3.0f}".format(value * RATIO)
        else:
            return "{:3.0f}".format(value)
    else:
        return None

@register.filter
def kg_conversion(value, client):
# converts kg to lbs according to client.units setting
    if value:
        RATIO = 0.45359237
        if client.units == "M":
            return "{:3.0f}".format(value * 1/RATIO)
        else:
            return "{:3.0f}".format(value)
    else:
        return None

@register.filter
def feet_conversion(value):
# converts feet+inches value from client.height_feet, client.height.inches according to client.units setting
    RATIO_FT = 30.48
    RATIO_IN = 2.54
    if value.units == "M":
        return "{:3.0f}".format(value.height_feet * RATIO_FT + value.height_inches * RATIO_IN)
    else:
        return str(value.height_feet) + "'" + str(value.height_inches) + '"'

@register.filter
def m_conversion(value, client):
# converts m value to inches according to client.units setting
    if value:
        RATIO = 39.701
        if client.units == "M":
            return "{:3.2f}".format(value * RATIO)
        else:
            return str(value)
    else:
        return None

@register.filter
def cm_conversion(value, client):
# converts cm value to inches according to client.units setting
    if value:
        RATIO = .3937
        if client.units == "M":
            return "{:3.2f}".format(value * RATIO)
        else:
            return str(value)
    else:
        return None

@register.filter
def weight_label(value):
# provides weight label according to client.units setting
    if value == 'M':
        return 'kg'
    else:
        return 'lbs'

@register.filter
def height_label(value):
# provides height label according to client.units setting
    if value == 'M':
        return 'cm'
    else:
        return ''


