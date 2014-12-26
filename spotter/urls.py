from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^index$', 'spotter.views.spotter_index', name='spotter_index'),
    url(r'^usage$', 'spotter.views.spotter_usage', name='spotter_usage'),
    url(r'^uploads$', 'spotter.views.spotter_uploads', name='spotter_uploads'),
    url(r'^program_upload$', 'spotter.views.spotter_program_upload', name='spotter_program_upload'),
    url(r'^program_create$', 'spotter.views.spotter_program_create', name='spotter_program_create'),
    url(r'^program_create/(?P<file>\w+)/$', 'spotter.views.spotter_program_create', name='spotter_program_create'),
#    url(r'^program_delete$', 'spotter.views.spotter_program_delete', name='spotter_program_delete'),
#    url(r'^program_delete/(?P<plan>\w+)/$', 'spotter.views.spotter_program_delete'),
    url(r'^program_sales_page$', 'spotter.views.spotter_sales_pages', name='spotter_sales_pages'),
    url(r'^program_sales_pages$', 'spotter.views.spotter_blitz_sales_pages', name='spotter_blitz_sales_pages'),
    url(r'^program_sales_page2$', 'spotter.views.spotter_sales_pages2', name='spotter_sales_pages2'),

    url(r'^workoutplan$', 'spotter.views.spotter_workoutplan', name='spotter_workoutplan'),
    url(r'^edit-workoutplan$', 'spotter.views.edit_workoutplan', name='edit_workoutplan'),

    url(r'^exercise_page$', 'spotter.views.spotter_exercise', name='spotter_exercise'),
    url(r'^exercise_page/(?P<slug>\w+)/$', 'spotter.views.spotter_exercise', name='spotter_exercise'),
    url(r'^custom_workoutset$', 'spotter.views.spotter_custom_set', name='spotter_custom_set'),
    url(r'^custom_exercise$', 'spotter.views.spotter_custom_exercise', name='spotter_custom_exercise'),

    url(r'^status_trainers$', 'spotter.views.spotter_status_trainers', name='spotter_status_trainers'),
    url(r'^assign_workoutplan$', 'spotter.views.assign_workoutplan', name='spotter_assign_workoutplan'),

    url(r'^download$', 'spotter.views.spotter_download', name='spotter_download'),
    url(r'^delete$', 'spotter.views.spotter_delete', name='spotter_delete'),
    url(r'^payments$', 'spotter.views.spotter_payments', name='spotter_payments'),
    url(r'^spotter_feed$', 'spotter.views.spotter_feed', name='spotter_feed'),
    url(r'^spotter_invites$', 'spotter.views.spotter_invites', name='spotter_invites'),

    )


from django.conf import settings
if settings.DEBUG != 4:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
