from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from settings import MEDIA_ROOT
import sys

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tocomprando.views.home', name='home'),
    # url(r'^tocomprando/', include('tocomprando.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #Main URLs
    url(r'^$', 'core.views.index',name='home'),
    url(r'register/$', 'core.views.register',name='register'),

    #Registration URLs
    url(r'^login/$', 'core.views.login',name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'},name='logout'),

)

urlpatterns += staticfiles_urlpatterns()

if len(sys.argv) >=2:
    if sys.argv[1] == 'runserver':
        #MEDIA's URLs.
        urlpatterns += patterns('',
            url(r'^media/(.*)$', 'django.views.static.serve',
             {'document_root': MEDIA_ROOT })
        )
