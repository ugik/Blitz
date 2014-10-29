from django import template
from base.models import BlitzInvitation

register = template.Library()

@register.filter
def member_price(value, member):
# determines price for member in blitz, if 1:1 blitz then blitz.price suffices, if Group blitz then need to check member invitation

    if member.blitz.recurring:
        return member.blitz.price

    invitation = BlitzInvitation.objects.filter(email=member.client.user.email)
    if invitation:
        if invitation[0].free:
            return 0
        else:
            return invitation[0].price

