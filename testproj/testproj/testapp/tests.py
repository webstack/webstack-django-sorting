from django.urls import reverse
from django.test import TestCase, Client

from . import models


class IndexTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("test_index")
        models.SecretFile.objects.create(filename="foo.txt", order=1, size=1024)
        models.SecretFile.objects.create(filename="bar.txt", order=2, size=512)

    def test_index(self):
        response = self.client.get(self.url)
        self.assertContains(response, "foo.txt")
        self.assertContains(response, "bar.txt")

    def test_sorting_direction(self):
        response = self.client.get(self.url, {"sort": "order", "dir": "asc"})
        values = ["<SecretFile: #1 foo.txt>", "<SecretFile: #2 bar.txt>"]
        self.assertQuerysetEqual(response.context["secret_files"], values)

        response = self.client.get(self.url, {"sort": "order", "dir": "desc"})
        values = ["<SecretFile: #2 bar.txt>", "<SecretFile: #1 foo.txt>"]
        self.assertQuerysetEqual(response.context["secret_files"], values)

        # Nothing wrong happens with an invalid direction and ASC is used
        response = self.client.get(self.url, {"sort": "order", "dir": "NOT"})
        values = ["<SecretFile: #1 foo.txt>", "<SecretFile: #2 bar.txt>"]
        self.assertQuerysetEqual(response.context["secret_files"], values)

    def test_sorting_argument(self):
        # Nothing wrong happens with invalid sort argument
        response = self.client.get(self.url, {"sort": "NOT EXISTING"})
        self.assertContains(response, "foo.txt")
