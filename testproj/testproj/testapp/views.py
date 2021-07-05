from django.shortcuts import render

from . import models


def secret_list(request):
    return render(
        request, "secret_list.html", {"secret_files": models.SecretFile.objects.all()}
    )


def secret_list_jinja2(request):
    return render(
        request, "secret_list.jinja2", {"secret_files": models.SecretFile.objects.all()}
    )


def secret_list_nulls_first(request):
    return render(
        request, "secret_list_nulls_first.html", {"secret_files": models.SecretFile.objects.all()}
    )


def secret_list_nulls_last(request):
    return render(
        request, "secret_list_nulls_last.html", {"secret_files": models.SecretFile.objects.all()}
    )
