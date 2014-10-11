from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^index$', 'helper.views.helper_index', name='helper_index'),
    url(r'^uploads$', 'helper.views.helper_uploads', name='helper_uploads'),
    url(r'^program_upload$', 'helper.views.helper_program_upload', name='helper_program_upload'),
    url(r'^program_create$', 'helper.views.helper_program_create', name='helper_program_create'),
    url(r'^program_create/(?P<file>\w+)/$', 'helper.views.helper_program_create', name='helper_program_create'),
    url(r'^program_delete$', 'helper.views.helper_program_delete', name='helper_program_delete'),
    url(r'^program_delete/(?P<plan>\w+)/$', 'helper.views.helper_program_delete'),
    url(r'^program_sales_page$', 'helper.views.helper_sales_pages', name='helper_sales_pages'),
    url(r'^program_sales_pages$', 'helper.views.helper_blitz_sales_pages', name='helper_blitz_sales_pages'),

    url(r'^workouts$', 'helper.views.helper_workouts', name='helper_workouts'),
    url(r'^exercise_page$', 'helper.views.helper_exercise', name='helper_exercise'),
    url(r'^exercise_page/(?P<slug>\w+)/$', 'helper.views.helper_exercise', name='helper_exercise'),
    url(r'^custom_workoutset$', 'helper.views.helper_custom_set', name='helper_custom_set'),
    url(r'^custom_exercise$', 'helper.views.helper_custom_exercise', name='helper_custom_exercise'),

    url(r'^pending_trainers$', 'helper.views.helper_pending_trainers', name='helper_pending_trainers'),
    url(r'^status_trainers$', 'helper.views.helper_status_trainers', name='helper_status_trainers'),
    url(r'^assign_workoutplan$', 'helper.views.assign_workoutplan', name='helper_assign_workoutplan'),

    url(r'^download$', 'helper.views.helper_download', name='helper_download'),
    url(r'^delete$', 'helper.views.helper_delete', name='helper_delete'),
    )


from django.conf import settings
if settings.DEBUG != 4:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
