from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'oa.views.index'),
    #url(r'tagtypes/add$', 'oa.views.add_tagtype'),
    url(r'tagtype/add$', 'oa.views.add_model'),
    url(r'tagtype/view/(?P<category_id>\d+)$', 'oa.views.tagtype'),
    #url(r'event$', 'oa.views.event'),
    url(r'event$', 'oa.views.model'),
    #url(r'event/add$', 'oa.views.add_event'),
    url(r'event/add$', 'oa.views.add_model'),
    #url(r'event/edit/(?P<event_id>\d+)$', 'oa.views.edit_event'),
    url(r'event/edit/(?P<model_id>\d+)$', 'oa.views.edit_model'),
    #url(r'event/view/(?P<event_id>\d+$)', 'oa.views.view_event'),
    url(r'event/view/(?P<model_id>\d+$)', 'oa.views.view_model'),
    #url(r'contact$', 'oa.views.contact'),
    url(r'contact$', 'oa.views.model'),
    #url(r'contact/add$', 'oa.views.add_contact'),
    url(r'contact/add$', 'oa.views.add_model'),
    #url(r'device/add$', 'oa.views.add_node'),
    url(r'device/add$', 'oa.views.add_model'),
    #url(r'device$', 'oa.views.node'),
    url(r'device$', 'oa.views.model'),
    url(r'device/edit/(?P<model_id>\d+)$', 'oa.views.edit_model'),
    #url(r'device/view/(?P<node_id>\d+$)', 'oa.views.view_node'),
    url(r'device/view/(?P<model_id>\d+$)', 'oa.views.view_model'),
    url(r'login$', 'oa.views.login_view'),
    url(r'logout$', 'oa.views.logout_view'),
    #url(r'alert/update$', 'oa.views.add_alert'),
    url(r'alert/update$', 'oa.views.add_model'),
    #url(r'alert$', 'oa.views.alert'),
    url(r'alert$', 'oa.views.model'),
    #url(r'alert/view/(?P<contact_id>)\d+$', 'oa.views.alert'),
    url(r'alert/view/(?P<model_id>)\d+$', 'oa.views.view_model'),
    url(r'tag/view/(?P<tag_id>\d+)$', 'oa.views.view_tag'),
    #url(r'tag/view/(?P<model_id>\d+)$', 'oa.views.view_model'),
    url(r'accountcreate$', 'oa.views.create_account'),
    url(r'^api/get_metadata$', 'oa.api.get_metadata'),
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'Oa.views.home', name='home'),
    # url(r'^Oa/', include('Oa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
