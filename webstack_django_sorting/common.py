"""
Common to Django tags (sorting_tags) and Jinja2 globals (jinja2_globals)
"""
from operator import attrgetter

from django.db.models import F
from django.http import Http404

from . import settings


def render_sort_anchor(request, field_name, title):
    get_params = request.GET.copy()
    sort_by = get_params.get("sort", None)
    if sort_by == field_name:
        # Render anchor link to next direction
        current_direction = settings.SORT_DIRECTIONS.get(
            get_params.get("dir", ""), settings.SORT_DIRECTIONS[""]
        )
        icon = current_direction["icon"]
        next_direction_code = current_direction["next"]
    else:
        icon = ""
        next_direction_code = "asc"

    # Not usual dict (can't update to replace)
    get_params["sort"] = field_name
    get_params["dir"] = next_direction_code
    url_append = "?" + get_params.urlencode() if get_params else ""
    return f'<a href="{request.path}{url_append}" title="{title}">{title}{icon}</a>'


def get_order_by_from_request(request):
    """
    Retrieve field used for sorting a queryset

    :param request: HTTP request
    :return: the sorted field name, prefixed with "-" if ordering is descending
    """
    sort_direction = request.GET.get("dir")
    field_name = (request.GET.get("sort") or "") if sort_direction else ""
    sort_sign = "-" if sort_direction == "desc" else ""
    return f"{sort_sign}{field_name}"


def need_python_sorting(queryset, order_by):
    if order_by.find("__") >= 0:
        # Python can't sort order_by with '__'
        return False

    # Python sorting if not a DB field
    field = order_by[1:] if order_by[0] == "-" else order_by
    field_names = [f.name for f in queryset.model._meta.get_fields()]
    return field not in field_names


def sort_queryset(queryset, order_by, null_ordering):
    """order_by is an Django ORM order_by argument"""

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
            raise ValueError

        reverse = True
        name = order_by[1:]
    else:
        reverse = False
        name = order_by

    if need_python_sorting(queryset, order_by):
        # Fallback on pure Python sorting (much slower on large data)
        if hasattr(queryset[0], name):
            return sorted(queryset, key=attrgetter(name), reverse=reverse)
        raise AttributeError

    ordering_exp = (F(name).desc if reverse else F(name).asc)(**null_ordering)
    return queryset.order_by(ordering_exp)


def get_null_ordering(request, default_template_ordering=None):
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
