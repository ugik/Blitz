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
import time
from datetime import datetime
import stripe

MEDIA_URL = getattr(settings, 'MEDIA_URL')
STATIC_URL = getattr(settings, 'STATIC_URL')

# utility function for payments
def balance(trainer=None, month=None, test=None, recurring_charge=None, apply=None):

    if trainer:
        trainer = Trainer.objects.get(pk=trainer)

    clients = []
    payments = []

    grand_total_paid = float(0.0)   # total paid across all clients in filter
    grand_total_value = float(0.0)  # total value of signups across all aclients in filter
    total_cost = float(0.0)         # total cost incurred per cleint
    total_paid = float(0.0)         # total payments processed per client
    total_value = float(0.0)        # total value of signup per client

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_charges = stripe.Charge.all(limit=9999)

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
            until_date = blitz.end_date    # until end of blitz if it's not recurring or in the past

        months = (len(list(rrule.rrule(rrule.MONTHLY, start_date, until=until_date))))   # months of usage

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

        # get charges with this client
        client_charges = list(filter(lambda d: 'client_id' in d['metadata'] and d['metadata']['client_id']==str(client.id), stripe_charges.data))

        if client_charges:
            for charge in client_charges:
                if not month or int(month) == datetime.fromtimestamp(charge.created).month:
                    if 'client_id' in charge.metadata:
                        payments.append({'amount': float(charge.amount)/100, 'status': charge.status, 
                             'created_at': time.ctime(int(charge.created)), 'xtion': charge.balance_transaction })
                        total_paid = float(total_paid) + float(charge.amount)/100
                        grand_total_paid += float(charge.amount)/100


        if client_charges:
            for charge in client_charges:
                refunds = stripe.Charge.retrieve(charge.id).refunds.all().data
                for refund in refunds:
                    if not month or int(month) == int(datetime.fromtimestamp(refund.created).month):

                        payments.append({'amount': float(refund.amount)/-100, 'status': 'refund',
                            'created_at': time.ctime(int(refund.created)), 'xtion': refund.balance_transaction })
                        total_paid = float(total_paid) - float(refund.amount)/100
                        grand_total_paid -= float(refund.amount)/100

        payment = 0
        note = error = None
 
        if not recurring_charge or float(total_cost)-float(total_paid)>0:

            # apply outstanding balance to credit card
            # must use both &charge and &apply params
            if recurring_charge and apply and client.balanced_account_uri:    
                meta = {"client_id": client.pk, "blitz_id": blitz.pk, 
                        "email": client.user.email}

                try:
                    debit_amount_str = "%d" % ((float(total_cost)-float(total_paid))*100)

                    debit = stripe.Charge.create(
                       amount = debit_amount_str,
                       currency = "usd",
                       customer = client.balanced_account_uri,
                       description = 'Blitz.us recurring payment',
                       metadata = meta
                    )

                    if debit.status != 'succeeded':
                        note = debit.status
                        error = True
                    else:
                        note = "%s payment of $%d" % (debit.status, (float(total_cost)-float(total_paid)) )

                except Exception as e:
                    note = "Error: %s" % e
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


