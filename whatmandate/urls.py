from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'votedata.views.different_elections', name='different_elections'),
    url(r'^election/(?P<election_id>\d+)/$', 'votedata.views.election_detail', name="election_detail"),
    # url(r'^whatmandate/', include('whatmandate.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
