from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'oa.views.index'),
        url(r'^manage/$', 'oa.OaViews.dropdownmanagement.index'),
        url(r'^manage/detail/(?P<type>\d{1})/$', 'oa.OaViews.dropdownmanagement.list'),
        url(r'^manage/save/$', 'oa.OaViews.dropdownmanagement.save'),
        url(r'^servers/add/$', 'oa.OaViews.servermanagement.add'),
	url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'Oa.views.home', name='home'),
    # url(r'^Oa/', include('Oa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
