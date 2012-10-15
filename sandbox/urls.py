from django.conf.urls import patterns, include, url
from django.contrib import admin

from sandbox.views import Index_View

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', (Index_View.as_view()), name="Index_View"),
    # url(r'^$', 'sandbox.views.home', name='home'),
    # url(r'^sandbox/', include('sandbox.foo.urls')),

    #include budget app urls
    (r'^budget/', include('budget.urls', namespace='budget', app_name='budget')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
