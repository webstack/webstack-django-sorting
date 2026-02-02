from collections.abc import Sequence
from typing import Any, Literal

from django.db.models import QuerySet
from django.http import HttpRequest
from markupsafe import Markup

from . import common


def sorting_anchor(
    request: HttpRequest,
    field_name: str,
    title: str,
    default_sort_order: Literal["asc", "desc"] = "asc",
) -> Markup:
    """Render a sorting anchor link for Jinja2 templates."""
    return Markup(common.render_sort_anchor(request, field_name, title, default_sort_order))


def sort_queryset(
    request: HttpRequest,
    queryset: QuerySet[Any],
    **context_var: str | None,
) -> QuerySet[Any] | Sequence[Any]:
    """Sort a queryset based on request parameters for Jinja2 templates."""
    order_by = common.get_order_by_from_request(request)
    null_ordering = common.get_null_ordering(request, context_var.get("nulls"))
    return common.sort_queryset(queryset, order_by, null_ordering)
