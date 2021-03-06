from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from base.api import UserResource, FeedItemResource
from tastypie.api import Api
from django.views.generic import TemplateView

handler500 = 'base.views.server_error'
handler404 = 'base.views.not_found_error'
handler403 = 'base.views.permission_denied_error'
handler400 = 'base.views.bad_request_error'

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(FeedItemResource())

urlpatterns = patterns('',
    (r'^spotter/', include('spotter.urls')),
)
urlpatterns += patterns(
    '',


    url("^dev/custom-trainer-page$", TemplateView.as_view(template_name="custon_trainer_page.html"), name="custom_trainer_page"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hijack/', include('hijack.urls')),

    url("^trainer/marc$", TemplateView.as_view(template_name="custom_trainer_page_marc.html")),
    url("^trainer/lexi$", TemplateView.as_view(template_name="custom_trainer_page_lexi.html")),

    url(r'^allclients$', 'base.views.all_clients', name='all_clients'),

    url(r'^post/gym/(?P<pk>\d+)$', 'base.views.single_post_gym', name='single_post_gym'),
    url(r'^post/comment/(?P<pk>\d+)$', 'base.views.single_post_comment', name='single_post_comment'),

    url(r'^login$', 'base.views.login_view', name='login_view'),
    url(r'^logout$', 'base.views.logout_view', name='logout_view'),
    url(r'^forgot-password$', 'base.views.forgot_password', name='forgot_password'),
    url(r'^forgot-password-sent$', 'base.views.forgot_password_sent', name='forgot_password_sent'),
    url(r'^reset-password$', 'base.views.reset_password', name='reset_password'),
    url(r'^reset-password-complete', 'base.views.reset_password_complete', name='reset_password_complete'),

    # url(r'^$', 'base.views.home', name='home'),
    url(r'^$', 'base.views.home', name='home'),
    url(r'^about$', 'base.views.about', name='about'),

    url(r'^profile$', 'base.views.my_profile', name='my_profile'),
    url(r'^profile/c/(?P<pk>\d+)$', 'base.views.client_profile', name='client_profile'),
    url(r'^profile/c/(?P<pk>\d+)/progress$', 'base.views.client_profile_progress', name='client_profile_progress'),
    url(r'^profile/c/(?P<pk>\d+)/history$', 'base.views.client_profile_history', name='client_profile_history'),
    url(r'^profile/c/(?P<pk>\d+)/checkins$', 'base.views.client_profile_checkins', name='client_profile_checkins'),
    url(r'^profile-basic$', 'base.views.set_up_profile_basic', name='profile_basic'),

    url(r'^profile/c/(?P<pk>\d+)/set-macros', 'base.views.set_client_macros', name='set_client_macros'),

    url(r'^client-signup$', 'base.views.client_signup', name='client_signup'),
    url(r'^client-setup$', 'base.views.client_setup', name='client_setup'),
    url(r'^client-setup/(?P<pk>\d+)$', 'base.views.client_blitz_setup', name='client_blitz_setup'),

    url(r'^client-checkin$', 'base.views.client_checkin', name='client_checkin'),

    url(r'^client-survey$', 'base.views.client_survey', name='client_survey'),
    url(r'^trainer-survey$', 'base.views.trainer_survey', name='trainer_survey'),

    url(r'^set-up-profile$', 'base.views.set_up_profile', name='set_up_profile'),

    url(r'^register-trainer$', 'base.views.trainer_signup', name='register_trainer'),
    url(r'^register-trainer-uploads/(?P<pk>\d+)$', 'base.views.trainer_signup_uploads', name='register_trainer_uploads'),

    url(r'^salespage$', 'base.views.my_salespages', name='my_salespages'),

    url(r'^program$', 'base.views.my_programs', name='my_blitz_program'),
    url(r'^view_program/(?P<pk>\d+)$', 'base.views.view_program', name='view_program'),

    url(r'^program/members$', 'base.views.my_blitz_members', name='my_blitz_members'),

    url(r'^dashboard$', 'base.views.trainer_dashboard', name='trainer_dashboard'),

    url(r'^log-workout/(?P<week_number>\d+)/(?P<day_char>\w+)$', 'base.views.log_workout', name='log_workout'),
    url(r'^preview-workout/(?P<workoutplan_pk>\d+)/(?P<week_number>\d+)/(?P<day_char>\w+)$', 'base.views.preview_workout', name='preview_workout'),

    url(r'^api/send-message-to-user/(?P<pk>\d+)', 'ff_messaging.views.send_message_to_user', name='send_message_to_user'),
    url(r'^api/new-comment', 'base.views.new_comment', name='new_comment'),
    url(r'^api/blitz_feed$', 'base.views.blitz_feed', name='blitz_feed'),

    url(r'^api/blitz_feed/viewed/mark$', 'base.views.blitz_feed_viewed', name='blitz_feed_viewed'),
    url(r'^api/blitz_feed/count$', 'base.views.get_unviewed_count', name='get_unviewed_count'),

    url(r'^api/blitz/(?P<pk>\d+)$', 'base.views.blitz', name='blitz'),
    url(r'^api/inbox_feed', 'ff_messaging.views.inbox_feed', name='inbox_feed'),
    url(r'^api/comment_like', 'base.views.comment_like', name='comment_like'),
    url(r'^api/comment_unlike', 'base.views.comment_unlike', name='comment_unlike'),
    url(r'^api/gym_session_like', 'base.views.gym_session_like', name='gym_session_like'),
    url(r'^api/gym_session_unlike', 'base.views.gym_session_unlike', name='gym_session_unlike'),
    url(r'^api/checkin_like', 'base.views.checkin_like', name='checkin_like'),
    url(r'^api/checkin_unlike', 'base.views.checkin_unlike', name='checkin_unlike'),
    url(r'^api/new-child-comment', 'base.views.new_child_comment', name='new_child_comment'),

    url(r'^api/save-sets', 'base.views.save_sets', name='save_sets'),

    url(r'^macros/get-macros-for-blitz-week', 'base.views.get_macros_for_blitz_week', name='get_macros_for_blitz_week'),
    url(r'^macros/undo-day', 'base.views.undo_macro_day', name='undo_macro_day'),
    url(r'^macros/save-day', 'base.views.save_macro_day', name='save_macro_day'),
    url(r'api/client_summary/(?P<pk>\w+)', 'base.views.client_summary', name='client_summary'),
    url(r'api/invitee_summary/(?P<pk>\w+)', 'base.views.invitee_summary', name='invitee_summary'),

    url(r'^trainer/dismiss-alert$', 'base.views.trainer_dismiss_alert', name='trainer_dismiss_alert'),
    url(r'^trainer/change-date$', 'base.views.trainer_change_date', name='trainer_change_date'),
    url(r'^trainer/spotter-edit$', 'base.views.spotter_edit', name='spotter_edit'),
    url(r'^trainer/profile/(?P<pk>\d+)$', 'base.views.trainer_profile', name='trainer_profile'),
    url(r'^trainer/blitz-macros-save$', 'base.views.blitz_macros_save', name='blitz_macros_save'),
    url(r'^trainer/client-macros-save$', 'base.views.client_macros_save', name='client_macros_save'),
    url(r'^trainer/invitee-macros-save$', 'base.views.invitee_macros_save', name='invitee_macros_save'),
    url(r'^trainer/client-setup$', 'base.views.client_setup', name='client_setup'),

    # todo: intro views namespaced as intro/[slug]
    url(r'^intro-data-1$', 'base.views.set_intro_1', name='set_intro_1'),

    (r'^api/', include(v1_api.urls)),

    url(r'^sales-blitz$', 'base.views.sales_blitz', name='sales_blitz'),
    url(r'^sales-blitz/(?P<plan_slug>\S+)', 'base.views.sales_blitz', name='sales_blitz'),

    url(r'^termsofuse$', 'base.views.terms_of_use', name='terms_of_use'),
    url(r'^privacypolicy$', 'base.views.privacy_policy', name='privacy_policy'),

    url(r'^profile/settings$', 'base.views.client_settings', name='client_settings'),
    url(r'^404$', 'base.views.page404', name="page404"),
    url(r'^500$', 'base.views.page500', name="page500"),

    url(r'^set-timezone$', 'base.views.set_timezone', name='set_timezone'),
    url(r'^set-units$', 'base.views.set_units', name='set_units'),

    url(r'^trainer/go-to-blitz', 'base.views.trainer_switch_blitz', name='trainer_switch_blitz'),

    url(r'^inbox$', 'ff_messaging.views.inbox', name='inbox'),
    url(r'^messages/new$', 'ff_messaging.views.new_message', name='new_message'),
    url(r'^messages/user/(?P<pk>\w+)/new$', 'ff_messaging.views.new_message_to_user', name='new_message_to_user'),
    url(r'^messages/thread/(?P<urlkey>\w+)$', 'ff_messaging.views.user_thread', name='user_thread'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),

    # blitz URLs
#    url(r'^blitz/(?P<url_slug>[a-zA-Z0-9_.-]+)/([\w|-]+)/create_account', 'base.views.create_account_hook', name='create_account_hook'),
    url(r'^blitz/(?P<pk>\d+)/([\w|-]+)/create_account', 'base.views.create_account_hook', name='create_account_hook'),

#    url(r'^blitz/(?P<url_slug>[a-zA-Z0-9_.-]+)/([\w|-]+)/payment_hook', 'base.views.payment_hook', name='payment_hook'),
    url(r'^blitz/(?P<pk>\d+)/([\w|-]+)/payment_hook', 'base.views.payment_hook', name='payment_hook'),

    url(r'^blitz-setup$', 'base.views.blitz_setup', name='blitz_setup'),

    url(r'^blitz_macros/(?P<pk>\d+)$', 'base.views.blitz_macros', name='blitz_macros'),
    url(r'^client_macros/(?P<pk>\d+)$', 'base.views.client_macros', name='client_macros'),

    url(r'^spotter_program_edit/(?P<pk>\d+)$', 'base.views.spotter_program_edit', name='spotter_program_edit'),

    url(r'^(?P<short_name>[a-zA-Z0-9_.-]+)/(?P<url_slug>[a-zA-Z0-9_.-]+)/signup$', 'base.views.blitz_signup', name="blitz_signup"),

    url(r'^(?P<short_name>[a-zA-Z0-9_.-]+)/(?P<url_slug>[a-zA-Z0-9_.-]+)/signup-complete$', 'base.views.blitz_signup_done', name='blitz_signup_done'),

    url(r'^(?P<short_name>[a-zA-Z0-9_.-]+)/signup$', 'base.views.default_blitz_signup', name="default_blitz_signup"),
    url(r'^signup-complete$', 'base.views.blitz_signup_done', name='blitz_signup_done'),

    url(r'^(?P<short_name>[a-zA-Z0-9_.-]+)$', 'base.views.default_blitz_page', name="default_blitz_page"),
    url(r'^(?P<short_name>[a-zA-Z0-9_.-]+)/(?P<url_slug>[a-zA-Z0-9_.-]+)$', 'base.views.blitz_page', name="blitz_page"),

#----------------------------------------

)


#    url(r'^errorlog$', 'base.views.errorlog', name='errorlog'),
