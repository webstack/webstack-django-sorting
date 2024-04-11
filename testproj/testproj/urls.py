from django.contrib import admin
from django.urls import path

from .testapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("list", views.secret_list, name="secret_list"),
    path("list_some_desc", views.secret_list_some_desc, name="secret_list_some_desc"),    
    path("nulls/first", views.secret_list_nulls_first, name="nulls_first"),
    path("nulls/last", views.secret_list_nulls_last, name="nulls_last"),
    path("jinja/list", views.jinja_secret_list, name="jinja_secret_list"),
    path("jinja/list_some_desc", views.jinja_secret_list_some_desc, name="jinja_secret_list_some_desc"),
    path(
        "jinja/nulls/first",
        views.jinja_secret_list_nulls_first,
        name="jinja_nulls_first",
    ),
    path(
        "jinja/nulls/last",
        views.jinja_secret_list_nulls_last,
        name="jinja_nulls_last",
    ),
    path("admin/", admin.site.urls),
]
