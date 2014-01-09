from django.shortcuts import render

from testproj.testapp import models

def test_index(request):
    return render(request, 'test_index.html', {
        'secret_files': models.SecretFile.objects.all()
    })

