from django.contrib import admin
from django.urls import path
from testproj.testapp import views

urlpatterns = [
    path("", views.test_index, name="test_index"),
    path("admin/", admin.site.urls),
]
