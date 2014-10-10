from django import template
register = template.Library()

def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

register.filter('active', active)

