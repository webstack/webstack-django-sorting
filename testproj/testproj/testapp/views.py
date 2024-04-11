from django.shortcuts import render

from . import models


def home(request):
    return render(request, "home.html")


def secret_list(request):
    return render(
        request, "secret_list.html", {"secret_files": models.SecretFile.objects.all()}
    )

def secret_list_some_desc(request):
    return render(
        request, "secret_list_some_desc.html", {"secret_files": models.SecretFile.objects.all()}
    )

def secret_list_nulls_first(request):
    return render(
        request,
        "secret_list_nulls_first.html",
        {"secret_files": models.SecretFile.objects.all()},
    )


def secret_list_nulls_last(request):
    return render(
        request,
        "secret_list_nulls_last.html",
        {"secret_files": models.SecretFile.objects.all()},
    )


def jinja_secret_list(request):
    return render(
        request, "secret_list.jinja2", {"secret_files": models.SecretFile.objects.all()}
    )

def jinja_secret_list_some_desc(request):
    return render(
        request, "secret_list_some_desc.jinja2", {"secret_files": models.SecretFile.objects.all()}
    )

def jinja_secret_list_nulls_first(request):
    return render(
        request,
        "secret_list_nulls_first.jinja2",
        {"secret_files": models.SecretFile.objects.all()},
    )


def jinja_secret_list_nulls_last(request):
    return render(
        request,
        "secret_list_nulls_last.jinja2",
        {"secret_files": models.SecretFile.objects.all()},
    )
