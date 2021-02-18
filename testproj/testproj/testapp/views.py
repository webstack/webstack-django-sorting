from django.shortcuts import render

from . import models


def secret_list(request):
    return render(
        request, "secret_list.html", {"secret_files": models.SecretFile.objects.all()}
    )
