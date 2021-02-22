from django.contrib import admin
from django.urls import path

from .testapp import views

urlpatterns = [
    path("", views.secret_list, name="secret_list"),
    path("jinja2", views.secret_list_jinja2, name="secret_list_jinja2"),
    path("admin/", admin.site.urls),
]
