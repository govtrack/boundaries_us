from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'', include('boundaries.urls')),
	(r'', include('maps.urls')),
	
    # Examples:
    # url(r'^$', 'boundaries_us.views.home', name='home'),
    # url(r'^boundaries_us/', include('boundaries_us.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
