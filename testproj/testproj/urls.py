from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'testproj.testapp.views.test_index'),
    url(r'^admin/', include(admin.site.urls)),
)
