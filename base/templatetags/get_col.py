from django import template
register = template.Library()

def get_col(value, counter):
  return value[counter]

def get_prior_col(value, counter):
  if counter>0:
      return value[counter-1]
  else:
      return value[counter]

register.filter('get_col', get_col)
register.filter('get_prior_col', get_prior_col)

