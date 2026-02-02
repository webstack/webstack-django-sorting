"""
Common to Django tags (sorting_tags) and Jinja2 globals (jinja2_globals)
"""

from operator import attrgetter
from typing import Any, Literal, Sequence

from django.db.models import F, QuerySet
from django.http import Http404, HttpRequest

from . import settings


def render_sort_anchor(
    request: HttpRequest,
    field_name: str,
    title: str,
    default_direction: Literal["asc", "desc"],
) -> str:
    """Render an HTML anchor tag for sorting a column."""
    get_params = request.GET.copy()
    sort_by = get_params.get("sort", None)
    css_class = ""
    icon = ""

    if sort_by == field_name:
        dir = get_params.get("dir", "")

        if dir == "asc":
            icon = settings.DEFAULT_SORT_UP
            css_class = settings.SORTING_CSS_CLASS_ASC
        elif dir == "desc":
            icon = settings.DEFAULT_SORT_DOWN
            css_class = settings.SORTING_CSS_CLASS_DESC

        # Mapping of direction transitions based on the default sort direction
        transition_map = {
            "asc": {"asc": "desc", "desc": "", "": "asc"},
            "desc": {"desc": "asc", "asc": "", "": "desc"},
        }
        next_direction_code = transition_map[default_direction].get(dir, "")

    else:
        next_direction_code = default_direction

    # Not usual dict (can't update to replace)
    get_params["sort"] = field_name
    get_params["dir"] = next_direction_code
    url_append = "?" + get_params.urlencode() if get_params else ""

    # Build the anchor tag with optional CSS class
    class_attr = f' class="{css_class}"' if css_class else ""
    return f'<a href="{request.path}{url_append}"{class_attr} title="{title}">{title}{icon}</a>'


def get_order_by_from_request(request: HttpRequest) -> str:
    """
    Retrieve field used for sorting a queryset.

    :param request: HTTP request
    :return: the sorted field name, prefixed with "-" if ordering is descending
    """
    sort_direction = request.GET.get("dir")
    field_name = (request.GET.get("sort") or "") if sort_direction else ""
    sort_sign = "-" if sort_direction == "desc" else ""
    return f"{sort_sign}{field_name}"


def need_python_sorting(queryset: QuerySet[Any], order_by: str) -> bool:
    """Check if Python sorting is needed (for non-database fields)."""
    if order_by.find("__") >= 0:
        # Python can't sort order_by with '__'
        return False

    # Python sorting if not a DB field
    field = order_by[1:] if order_by[0] == "-" else order_by
    field_names = [f.name for f in queryset.model._meta.get_fields()]
    return field not in field_names


def sort_queryset(
    queryset: QuerySet[Any],
    order_by: str,
    null_ordering: dict[str, bool],
) -> QuerySet[Any] | Sequence[Any]:
    """
    Sort a queryset by the given field.

    :param queryset: The queryset to sort
    :param order_by: Django ORM order_by argument (e.g., "name" or "-name")
    :param null_ordering: Dict with nulls_first or nulls_last setting
    :return: Sorted queryset or list (if Python sorting is used)
    """
    if not order_by:
        # In this case the queryset can't be ordered (no field name specified)
        # even though nulls ordering is set
        return queryset

    # The field name can be prefixed by the minus sign and we need to
    # extract this information if we want to sort on simple object
    # attributes
    if order_by[0] == "-":
        if len(order_by) == 1:
            # Prefix without field name
            raise ValueError("Order by prefix without field name")

        reverse = True
        name = order_by[1:]
    else:
        reverse = False
        name = order_by

    if need_python_sorting(queryset, order_by):
        # Fallback on pure Python sorting (much slower on large data)
        if hasattr(queryset[0], name):
            return sorted(queryset, key=attrgetter(name), reverse=reverse)
        raise AttributeError(f"Object has no attribute '{name}'")

    ordering_exp = (F(name).desc if reverse else F(name).asc)(**null_ordering)
    return queryset.order_by(ordering_exp)


def get_null_ordering(
    request: HttpRequest,
    default_template_ordering: str | None = None,
) -> dict[str, bool]:
    """
    Get null ordering configuration from request or template default.

    :param request: HTTP request
    :param default_template_ordering: Default ordering from template ("first" or "last")
    :return: Dict with nulls_first or nulls_last setting, or empty dict
    """
    # Prioritize changes in URL parameter over the default template variable
    nulls_value = request.GET.get("nulls", default_template_ordering)
    if nulls_value:
        if nulls_value not in ("first", "last"):
            if settings.INVALID_FIELD_RAISES_404:
                raise Http404("The nulls query paramater should be 'first' or 'last'.")

            # Else ignores invalid values
            return {}

        return {f"nulls_{nulls_value}": True}

    return {}
