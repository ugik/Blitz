from django.contrib import admin
from base.models import Trainer, Client, Blitz, BlitzMember, BlitzInvitation, GymSession, CompletedSet, Comment, CommentLike, FeedItem, TrainerAlert, MacroDay, SalesPageContent, CheckIn, Heading

admin.site.register(Trainer)
admin.site.register(Client)
admin.site.register(Blitz)
admin.site.register(BlitzMember)
admin.site.register(BlitzInvitation)
admin.site.register(FeedItem)
admin.site.register(GymSession)
admin.site.register(CompletedSet)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(TrainerAlert)
admin.site.register(MacroDay)
admin.site.register(SalesPageContent)
admin.site.register(CheckIn)
admin.site.register(Heading)

