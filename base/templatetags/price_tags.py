from django import template
from base.models import BlitzInvitation

register = template.Library()

@register.filter
def member_price(value, member):
# determines price for member in blitz, if 1:1 blitz then blitz.price suffices, if Group blitz then need to check member invitation

    return member.blitz.price

    # TODO: clean this up, invitation is deleted on signup

    if not member.blitz.group:
        return member.blitz.price

    invitation = BlitzInvitation.objects.filter(email=member.client.user.email)
    if invitation:
        if invitation[0].free:
            return 0
        else:
            return invitation[0].price

    else:
        return member.blitz.price


