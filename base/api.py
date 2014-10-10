from tastypie.resources import ModelResource
from tastypie import fields

from base.models import FeedItem, Client, Trainer, Blitz
from django.contrib.auth.models import User

class UserResource(ModelResource):
    is_trainer = fields.BooleanField()
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'user_type', 'is_trainer', 'display_name', 'headshot_url', 'blitz']
        allowed_methods = ['get']

class FeedItemResource(ModelResource):
    class Meta:
        queryset = FeedItem.objects.all().order_by('-pub_date')
        resource_name = 'feeditem'
