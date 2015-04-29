from base.models import Trainer, Client, BlitzMember, BlitzInvitation

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from workouts import utils as workout_utils
from workouts.models import WorkoutSet, Lift, Workout, ExerciseCustom
from base.templatetags import units_tags

from datetime import date, timedelta
from dateutil import rrule
import hashlib
import datetime
import json
import itertools
import random
import string
import balanced

MEDIA_URL = getattr(settings, 'MEDIA_URL')
STATIC_URL = getattr(settings, 'STATIC_URL')

# utility function for payments
def balance(trainer=None, month=None, test=None, charge=None, apply=None):

    if trainer:
        trainer = Trainer.objects.get(pk=trainer)

    clients = []
    payments = []

    grand_total_paid = float(0.0)   # total paid across all clients in filter
    grand_total_value = float(0.0)  # total value of signups across all aclients in filter
    total_cost = float(0.0)         # total cost incurred per cleint
    total_paid = float(0.0)         # total payments processed per client
    total_value = float(0.0)        # total value of signup per client

    for client in Client.objects.all():

        blitz = client.get_blitz()
        if not blitz:  # ignore clients not enrolled
            continue
        if trainer and trainer != blitz.trainer:  # trainer filter (optional)
            continue
        # by default ignore test/free users
        if not test and client.balanced_account_uri == '':   # ignore clients with no cc reference
            continue

        if client.date_created < blitz.begin_date:   # use blitz begin date if client signed up prior
            start_date = blitz.begin_date
        else:
            start_date = client.date_created

        if date.today < blitz.end_date or blitz.recurring:   # use today if blitz hasn't ended yet
            until_date = date.today()
        else:
            until_date = blitz.end_date()    # until end of blitz if it's not recurring or in the past

        months = abs((until_date - start_date).days)/7/4    # months of usage (month = 4 workout weeks)

        membership = client.blitzmember_set.all()
        if not membership[0].price:   # if there was no special invitation price
            if blitz.price_model == "R":   # recurring price model
                total_cost = months * blitz.price if blitz.price else 0
                total_value = float(blitz.num_weeks() / 4 * blitz.price) if blitz.price else 0
            else:
                total_cost = total_value = blitz.price if blitz.price else 0
        else:
            if blitz.price_model == "R":
                total_cost = months * membership[0].price
                total_value = float(blitz.num_weeks() / 4 * membership[0].price)        
            else:
                total_cost = total_value = membership[0].price

        grand_total_value += float(total_value)

        debits = balanced.Debit.query.filter(balanced.Debit.f.meta.client_id == client.pk)
        if debits:
            for debit in debits:
                if not month or int(month) == int(debit.created_at[5:7]):
                    if 'client_id' in debit.meta:
                        payments.append({'amount': float(debit.amount)/100, 'status': debit.status, 
                             'created_at': debit.created_at[0:10], 'xtion': debit.transaction_number })
                        total_paid = float(total_paid) + float(debit.amount)/100
                        grand_total_paid += float(debit.amount)/100

        refunds = balanced.Refund.query.filter(balanced.Refund.f.meta.client_id == client.pk)
        if refunds:
            for refund in refunds:
                if not month or int(month) == int(refund.created_at[5:7]):

                    if 'client_id' in debit.meta:
                        payments.append({'amount': float(debit.amount)/-100, 'status': debit.status, 
                             'created_at': debit.created_at[0:10], 'xtion': debit.transaction_number })
                        total_paid = float(total_paid) - float(debit.amount)/100
                        grand_total_paid -= float(debit.amount)/100

        payment = 0
        note = error = None
 
        if not charge or float(total_cost)-float(total_paid)>0:

            # apply outstanding balance to cc
            if charge and apply and client.balanced_account_uri:    # must use both &charge and &apply params
                meta = {"client_id": client.pk, "blitz_id": blitz.pk, 
                        "email": client.user.email}

                try:
                    card = balanced.Card.fetch(client.balanced_account_uri)
                    debit_amount_str = "%d" % ((float(total_cost)-float(total_paid))*100)
                    debit = card.debit(appears_on_statement_as = 'Blitz.us payment',
                                       amount = debit_amount_str, description='Blitz.us payment', meta=meta)

                    if debit.status != 'succeeded':
                        note = debit.failure_reason
                        error = True
                    else:
                        note = "%s payment of $%d" % (debit.status, (float(total_cost)-float(total_paid)) )

                except Exception as e:
                    note = "Error: %s" % e.status
                    error = True

                payment = (float(total_cost)-float(total_paid)) if not error else 0

            clients.append({'client':client, 'blitz': blitz, 'membership': membership[0], 'payment': payment,
                            'start':start_date, 'months': months, 'payments': payments, 'note': note,
                            'total_cost': '%.2f' % total_cost, 'total_paid': '%.2f' % total_paid, 
                            'total_value': '%.2f' % total_value,
                            'due': '%.2f' % (float(total_cost)-float(total_paid))})

        payments = []
        total_cost = total_paid = 0

    net = float(grand_total_paid * 0.85)
    
    return {'test': test, 'charge': charge, 'apply': apply, 'month': month,
            'trainer': trainer, 'clients': clients, 
            'total': grand_total_paid, 'total_value': grand_total_value, 'net': net }


