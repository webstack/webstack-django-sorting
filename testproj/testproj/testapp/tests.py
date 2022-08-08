from django.test import TestCase
from django.urls import reverse
from webstack_django_sorting import settings

from . import models


class IndexTest(TestCase):
    def setUp(self):
        self.url = reverse("secret_list")

        models.SecretFile.objects.create(filename="foo.txt", order=1, size=1024)
        models.SecretFile.objects.create(filename="bar.txt", order=2, size=512)

    def test_list(self):
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


class NullsTestCase(TestCase):
    def setUp(self):
        self.nulls_first_url = reverse("nulls_first")
        self.nulls_last_url = reverse("nulls_last")

        models.SecretFile.objects.create(filename="foo.txt", order=1, size=1024)
        models.SecretFile.objects.create(filename="bar.txt", order=2, size=512)

    def test_sorting_nulls_first(self):
        """Verify None sorted field_name is in first places when sorting in asc and desc order"""

        models.SecretFile.objects.create(filename=None, order=3, size=512)
        # asc order
        values = [
            "<SecretFile: #3 None>",
            "<SecretFile: #2 bar.txt>",
            "<SecretFile: #1 foo.txt>",
        ]
        response = self.client.get(
            self.nulls_first_url, {"sort": "filename", "nulls": "first", "dir": "asc"}
        )
        self.assertQuerysetEqual(list(response.context["secret_files"]), values)

        # desc order
        values = [
            "<SecretFile: #3 None>",
            "<SecretFile: #1 foo.txt>",
            "<SecretFile: #2 bar.txt>",
        ]
        response = self.client.get(
            self.nulls_first_url,
            {"sort": "filename", "nulls": "first", "dir": "desc"},
        )
        self.assertQuerysetEqual(list(response.context["secret_files"]), values)

    def test_sorting_nulls_last(self):
        """Verify None sorted field_name is in last places when sorting in asc and desc order."""

        models.SecretFile.objects.create(filename=None, order=3, size=512)
        # asc order
        values = [
            "<SecretFile: #2 bar.txt>",
            "<SecretFile: #1 foo.txt>",
            "<SecretFile: #3 None>",
        ]
        response = self.client.get(
            self.nulls_last_url, {"sort": "filename", "nulls": "last", "dir": "asc"}
        )
        self.assertQuerysetEqual(list(response.context["secret_files"]), values)

        # desc order
        values = [
            "<SecretFile: #1 foo.txt>",
            "<SecretFile: #2 bar.txt>",
            "<SecretFile: #3 None>",
        ]
        response = self.client.get(
            self.nulls_last_url, {"sort": "filename", "nulls": "last", "dir": "desc"}
        )
        self.assertQuerysetEqual(list(response.context["secret_files"]), values)

    def test_check_values(self):
        # Internal INVALID_FIELD_RAISES_404 is set at loading (no override_settings)
        saved = settings.INVALID_FIELD_RAISES_404
        try:
            settings.INVALID_FIELD_RAISES_404 = True
            response = self.client.get(
                self.nulls_last_url, {"sort": "filename", "nulls": "foo", "dir": "asc"}
            )
        finally:
            settings.INVALID_FIELD_RAISES_404 = saved

        self.assertEqual(response.status_code, 404)
