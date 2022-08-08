from django.contrib import admin
from django.urls import path

from .testapp import views

urlpatterns = [
    path("", views.secret_list, name="secret_list"),
    path("nulls/first", views.secret_list_nulls_first, name="nulls_first"),
    path("nulls/last", views.secret_list_nulls_last, name="nulls_last"),
    path("jinja", views.jinja_secret_list, name="jinja_secret_list"),
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
