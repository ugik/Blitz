from django import template
register = template.Library()

def get_range(value, start=0):
  return range(start, value)

register.filter('get_range', get_range)
