from django.http import HttpRequest, QueryDict
from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse

from webstack_django_sorting import settings
from webstack_django_sorting.common import render_sort_anchor

from . import models


class SortingTest(TestCase):
    """Test Django template sorting functionality."""

    def setUp(self):
        self.url = reverse("secret_list")
        self.foo_file = models.SecretFile.objects.create(filename="foo.txt", order=1, size=1024)
        self.bar_file = models.SecretFile.objects.create(filename="bar.txt", order=2, size=512)

    def test_list(self):
        response = self.client.get(self.url)
        self.assertContains(response, "foo.txt")
        self.assertContains(response, "bar.txt")

    def test_sorting_direction(self):
        response = self.client.get(self.url, {"sort": "order", "dir": "asc"})
        self.assertQuerySetEqual(response.context["secret_files"], [self.foo_file, self.bar_file])

        response = self.client.get(self.url, {"sort": "order", "dir": "desc"})
        self.assertQuerySetEqual(response.context["secret_files"], [self.bar_file, self.foo_file])

        # Invalid direction defaults to asc
        response = self.client.get(self.url, {"sort": "order", "dir": "INVALID"})
        self.assertQuerySetEqual(response.context["secret_files"], [self.foo_file, self.bar_file])

    def test_sorting_by_different_fields(self):
        """Test sorting works on multiple field types."""
        response = self.client.get(self.url, {"sort": "size", "dir": "asc"})
        self.assertQuerySetEqual(response.context["secret_files"], [self.bar_file, self.foo_file])

        response = self.client.get(self.url, {"sort": "filename", "dir": "asc"})
        self.assertQuerySetEqual(response.context["secret_files"], [self.bar_file, self.foo_file])

    def test_invalid_sort_field(self):
        """Invalid sort field is handled gracefully."""
        response = self.client.get(self.url, {"sort": "NOT_EXISTING"})
        self.assertContains(response, "foo.txt")

    def test_empty_queryset(self):
        """Sorting an empty queryset doesn't raise errors."""
        models.SecretFile.objects.all().delete()
        response = self.client.get(self.url, {"sort": "order", "dir": "asc"})
        self.assertEqual(response.status_code, 200)


class NullsOrderingTest(TestCase):
    """Test NULL value ordering."""

    def setUp(self):
        self.foo_file = models.SecretFile.objects.create(filename="foo.txt", order=1, size=1024)
        self.bar_file = models.SecretFile.objects.create(filename="bar.txt", order=2, size=512)
        self.none_file = models.SecretFile.objects.create(filename=None, order=3, size=512)

    def test_nulls_first(self):
        """NULL values appear first when nulls=first."""
        url = reverse("nulls_first")
        response = self.client.get(url, {"sort": "filename", "nulls": "first", "dir": "asc"})
        self.assertQuerySetEqual(
            list(response.context["secret_files"]),
            [self.none_file, self.bar_file, self.foo_file],
        )

    def test_nulls_last(self):
        """NULL values appear last when nulls=last."""
        url = reverse("nulls_last")
        response = self.client.get(url, {"sort": "filename", "nulls": "last", "dir": "asc"})
        self.assertQuerySetEqual(
            list(response.context["secret_files"]),
            [self.bar_file, self.foo_file, self.none_file],
        )

    def test_invalid_nulls_param_raises_404(self):
        """Invalid nulls parameter raises 404 when configured."""
        url = reverse("nulls_last")
        saved = settings.INVALID_FIELD_RAISES_404
        try:
            settings.INVALID_FIELD_RAISES_404 = True
            response = self.client.get(url, {"sort": "filename", "nulls": "invalid", "dir": "asc"})
            self.assertEqual(response.status_code, 404)
        finally:
            settings.INVALID_FIELD_RAISES_404 = saved


class Jinja2Test(TestCase):
    """Test Jinja2 template support."""

    def setUp(self):
        self.foo_file = models.SecretFile.objects.create(filename="foo.txt", order=1, size=1024)
        self.bar_file = models.SecretFile.objects.create(filename="bar.txt", order=2, size=512)

    def test_jinja_sorting(self):
        """Jinja2 templates sort correctly."""
        url = reverse("jinja_secret_list")

        # Ascending
        response = self.client.get(url, {"sort": "order", "dir": "asc"})
        content = response.content.decode()
        self.assertLess(content.find("foo.txt"), content.find("bar.txt"))

        # Descending
        response = self.client.get(url, {"sort": "order", "dir": "desc"})
        content = response.content.decode()
        self.assertGreater(content.find("foo.txt"), content.find("bar.txt"))

    def test_jinja_nulls_ordering(self):
        """Jinja2 templates handle NULL ordering."""
        models.SecretFile.objects.create(filename=None, order=3, size=512)

        response = self.client.get(
            reverse("jinja_nulls_first"), {"sort": "filename", "nulls": "first", "dir": "asc"}
        )
        content = response.content.decode()
        self.assertLess(content.find("bar.txt"), content.find("foo.txt"))


class RenderSortAnchorTest(TestCase):
    """Test the render_sort_anchor function - core anchor rendering logic."""

    def _make_request(self, query_params=None):
        request = HttpRequest()
        request.path = "/test/"
        request.GET = QueryDict(mutable=True)
        if query_params:
            for key, value in query_params.items():
                request.GET[key] = value
        return request

    def test_basic_anchor(self):
        """Anchor renders with correct href and title."""
        request = self._make_request()
        result = render_sort_anchor(request, "name", "Name", "asc")
        self.assertIn('href="/test/?sort=name&dir=asc"', result)
        self.assertIn('title="Name"', result)
        self.assertIn(">Name</a>", result)

    def test_three_way_toggle(self):
        """Test the three-way sorting toggle: none -> asc -> desc -> none."""
        # No sort -> asc (with asc default)
        result = render_sort_anchor(self._make_request(), "name", "Name", "asc")
        self.assertIn("dir=asc", result)

        # asc -> desc
        result = render_sort_anchor(
            self._make_request({"sort": "name", "dir": "asc"}), "name", "Name", "asc"
        )
        self.assertIn("dir=desc", result)
        self.assertIn(settings.DEFAULT_SORT_UP, result)

        # desc -> none (empty dir)
        result = render_sort_anchor(
            self._make_request({"sort": "name", "dir": "desc"}), "name", "Name", "asc"
        )
        self.assertIn(settings.DEFAULT_SORT_DOWN, result)
        self.assertNotIn("dir=asc", result)
        self.assertNotIn("dir=desc", result)

    def test_desc_default_direction(self):
        """With desc default, first click sorts descending."""
        result = render_sort_anchor(self._make_request(), "name", "Name", "desc")
        self.assertIn("dir=desc", result)

    def test_css_class_support(self):
        """CSS classes are added to anchor when configured."""
        saved_asc = settings.SORTING_CSS_CLASS_ASC
        saved_desc = settings.SORTING_CSS_CLASS_DESC
        try:
            settings.SORTING_CSS_CLASS_ASC = "sorted-asc"
            settings.SORTING_CSS_CLASS_DESC = "sorted-desc"

            result = render_sort_anchor(
                self._make_request({"sort": "name", "dir": "asc"}), "name", "Name", "asc"
            )
            self.assertIn('class="sorted-asc"', result)

            result = render_sort_anchor(
                self._make_request({"sort": "name", "dir": "desc"}), "name", "Name", "asc"
            )
            self.assertIn('class="sorted-desc"', result)
        finally:
            settings.SORTING_CSS_CLASS_ASC = saved_asc
            settings.SORTING_CSS_CLASS_DESC = saved_desc


class TemplateTagParsingTest(TestCase):
    """Test Django template tag parsing."""

    def _render(self, template_str, context_vars=None):
        template = Template(template_str)
        request = HttpRequest()
        request.path = "/test/"
        request.GET = QueryDict()
        context = Context({"request": request, **(context_vars or {})})
        return template.render(context)

    def test_anchor_with_quoted_title(self):
        result = self._render('{% load sorting_tags %}{% anchor field_name "Title" %}')
        self.assertIn("field_name", result)
        self.assertIn("Title", result)

    def test_anchor_minimal(self):
        """Field name is capitalized when no title given."""
        result = self._render("{% load sorting_tags %}{% anchor field_name %}")
        self.assertIn("Field_name", result)

    def test_anchor_with_variable_title(self):
        result = self._render(
            "{% load sorting_tags %}{% anchor field_name my_title %}",
            {"my_title": "Dynamic Title"},
        )
        self.assertIn("Dynamic Title", result)

    def test_anchor_with_desc_default(self):
        result = self._render('{% load sorting_tags %}{% anchor field_name "Title" "desc" %}')
        self.assertIn("dir=desc", result)
