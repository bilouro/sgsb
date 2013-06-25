from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sgsb.views.home', name='home'),
    url(r'^cadastro/', include('cadastro.urls')),

    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'cadastro.views.inicial'),

    # deve ficar no final para que as personalizacoes
    # por aplicacao sejao prioritarias
    #LIST
    (r'^(?P<app_name>\w+)/(?P<model_name>\w+)/list.(?P<return_type>(json|xml))$',
     'cadastro.generic_views.generic_get_json' ),
    #GET ONE
    (r'^(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<instance_id>\d+).(?P<return_type>(json|xml))$',
     'cadastro.generic_views.generic_get_json' ),
    #EDIT
    (r'^(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<instance_id>\d+)/edit$', 'cadastro.generic_views.generic_add_edit'),
    #DELETE
    (r'^(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<instance_id>\d+)/delete$', 'cadastro.generic_views.generic_delete'),
    #ADD
    (r'^(?P<app_name>\w+)/(?P<model_name>\w+)/add[/]{0,1}$', 'cadastro.generic_views.generic_add_edit'),

)
