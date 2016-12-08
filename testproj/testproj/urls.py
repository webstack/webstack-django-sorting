from django.conf.urls import url
from django.contrib import admin
from testproj.testapp import views

urlpatterns = [
    url(r'^$', views.test_index),
    url(r'^admin/', admin.site.urls),
]
