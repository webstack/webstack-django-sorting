from django.test import TestCase
from django.urls import reverse
from webstack_django_sorting import settings

from . import models


class IndexTest(TestCase):
    def setUp(self):
        self.url = reverse("secret_list")

        self.foo_file = models.SecretFile.objects.create(
            filename="foo.txt", order=1, size=1024
        )
        self.bar_file = models.SecretFile.objects.create(
            filename="bar.txt", order=2, size=512
        )

    def test_list(self):
        response = self.client.get(self.url)
        self.assertContains(response, "foo.txt")
        self.assertContains(response, "bar.txt")

    def test_sorting_direction(self):
        response = self.client.get(self.url, {"sort": "order", "dir": "asc"})
        values = [self.foo_file, self.bar_file]
        self.assertQuerySetEqual(response.context["secret_files"], values)

        response = self.client.get(self.url, {"sort": "order", "dir": "desc"})
        values = [self.bar_file, self.foo_file]
        self.assertQuerySetEqual(response.context["secret_files"], values)

        # Nothing wrong happens with an invalid direction and ASC is used
        response = self.client.get(self.url, {"sort": "order", "dir": "NOT"})
        values = [self.foo_file, self.bar_file]
        self.assertQuerySetEqual(response.context["secret_files"], values)

    def test_sorting_argument(self):
        # Nothing wrong happens with invalid sort argument
        response = self.client.get(self.url, {"sort": "NOT EXISTING"})
        self.assertContains(response, "foo.txt")


class NullsTestCase(TestCase):
    def setUp(self):
        self.nulls_first_url = reverse("nulls_first")
        self.nulls_last_url = reverse("nulls_last")

        self.foo_file = models.SecretFile.objects.create(
            filename="foo.txt", order=1, size=1024
        )
        self.bar_file = models.SecretFile.objects.create(
            filename="bar.txt", order=2, size=512
        )
        self.none_file = models.SecretFile.objects.create(
            filename=None, order=3, size=512
        )

    def test_sorting_nulls_first(self):
        """Verify None sorted field_name is in first places when sorting in asc and desc order"""

        # asc order
        values = [self.none_file, self.bar_file, self.foo_file]
        response = self.client.get(
            self.nulls_first_url, {"sort": "filename", "nulls": "first", "dir": "asc"}
        )
        self.assertQuerySetEqual(list(response.context["secret_files"]), values)

        # desc order
        values = [self.none_file, self.foo_file, self.bar_file]
        response = self.client.get(
            self.nulls_first_url,
            {"sort": "filename", "nulls": "first", "dir": "desc"},
        )
        self.assertQuerySetEqual(list(response.context["secret_files"]), values)

    def test_sorting_nulls_last(self):
        """Verify None sorted field_name is in last places when sorting in asc and desc order."""

        # asc order
        values = [self.bar_file, self.foo_file, self.none_file]
        response = self.client.get(
            self.nulls_last_url, {"sort": "filename", "nulls": "last", "dir": "asc"}
        )
        self.assertQuerySetEqual(list(response.context["secret_files"]), values)

        # desc order
        values = [self.foo_file, self.bar_file, self.none_file]
        response = self.client.get(
            self.nulls_last_url, {"sort": "filename", "nulls": "last", "dir": "desc"}
        )
        self.assertQuerySetEqual(list(response.context["secret_files"]), values)

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
