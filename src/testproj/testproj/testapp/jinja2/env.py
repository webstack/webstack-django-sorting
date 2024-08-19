from jinja2.environment import Environment

from django.template.defaultfilters import yesno
from django.templatetags.static import static
from webstack_django_sorting.jinja2_globals import (
    sorting_anchor,
    sort_queryset,
)


class JinjaEnvironment(Environment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filters["yesno"] = yesno
        self.globals["sorting_anchor"] = sorting_anchor
        self.globals["sort_queryset"] = sort_queryset
        self.globals["static"] = static
