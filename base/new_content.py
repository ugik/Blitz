"""
Contains factories for new content and post save signals
Should probably move to either/or
"""

from base.models import Comment, FeedItem, CommentLike, GymSessionLike, CheckIn, CheckInLike
from base.emails import new_child_comment, gym_session_comment
from base.notifications import new_child_comment, gym_session_comment

from django.db.models.signals import post_save

import datetime

def create_new_parent_comment(user, comment_text, pub_date, image=None, blitz=None):
    # Create a new parent comment, this implies creating a feed item too

    comment = Comment.objects.create(user=user, text=comment_text, date_and_time=pub_date, image=image)
    if not blitz:
        feeditem = FeedItem.objects.create(blitz=user.blitz, content_object=comment, pub_date=pub_date)
    else:
        feeditem = FeedItem.objects.create(blitz=blitz, content_object=comment, pub_date=pub_date)

    return comment, feeditem

    # todo: send emails?

def add_child_to_comment(parent, user, comment_text, pub_date):

    comment = Comment.objects.create(user=user, text=comment_text, date_and_time=pub_date, parent_comment=parent)

    # send alerts
    other_children = list(parent.comment_set.all())
    authors = { c.user for c in [parent] + other_children }
    authors.remove(user)
    for author in authors:
        new_child_comment(author, commenter=user, comment=comment)

    return comment

def add_comment_to_gym_session(gym_session, user, comment_text, pub_date):

    comment = Comment.objects.create(user=user, text=comment_text, date_and_time=pub_date, gym_session=gym_session)

    # alert to gym session user
    if user != gym_session.client.user:
        gym_session_comment(gym_session.client.user, commenter=user, comment=comment)

    # alerts to other comments
    other_children = list(gym_session.gymsessioncomments.all())
    authors = { c.user for c in other_children }
    authors.remove(user)
    for author in authors:
        new_child_comment(author, commenter=user, comment=comment)

    return comment

def add_comment_to_checkin(checkin, user, comment_text, pub_date):

    comment = Comment.objects.create(user=user, text=comment_text, date_and_time=pub_date, checkin=checkin)

    # alert to gym session user
    if user != checkin.client.user:
        checkin_comment(checkin.client.user, commenter=user, comment=comment)

    # alerts to other comments
    other_children = list(checkin.checkincomments.all())
    authors = { c.user for c in other_children }
    authors.remove(user)
    for author in authors:
        new_child_comment(author, commenter=user, comment=comment)

    return comment

def add_like_to_comment(comment, user, pub_date):

    commentlike = CommentLike.objects.create(comment=comment, user=user, date_and_time=pub_date)
    return commentlike

def add_like_to_gym_session(gym_session, user, pub_date):

    gymsessionlike = GymSessionLike.objects.create(gym_session=gym_session, user=user, date_and_time=pub_date)
    return gymsessionlike

def add_like_to_checkin(checkin, user, pub_date):

    checkinlike = CheckInLike.objects.create(checkin=checkin, user=user, date_and_time=pub_date)
    return checkinlike


def finalize_gym_session(blitz, gym_session, pub_date):
    """
    call after a session is finalized - analagous to a post save signal
    which is probably what we should do in the first place
    """
    gym_session.is_logged = True
    gym_session.save()
    feed_item = FeedItem.objects.create(blitz=blitz, content_object=gym_session,
        pub_date=pub_date)


