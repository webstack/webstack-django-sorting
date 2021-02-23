"""
Common to Django tags (sorting_tags) and Jinja2 globals (jinja2_globals)
"""
from urllib.parse import urlencode
from operator import attrgetter

from .settings import SORT_DIRECTIONS


def render_sort_anchor(request, field_name, title):
    sort_by = request.GET.get("sort", "")
    if sort_by == field_name:
        # Render anchor link to next direction
        sort_direction = SORT_DIRECTIONS[request.GET.get("dir", "")]
        next_direction_code = sort_direction["next"]
        icon = sort_direction["icon"]
    else:
        # Just a fast code path
        next_direction_code = "asc"
        icon = ""

    url_sort_by = urlencode({"sort": field_name})
    url_append = f"?{url_sort_by}"
    if next_direction_code:
        url_sort_direction = urlencode({"dir": next_direction_code})
        url_append += f"&{url_sort_direction}"

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


def sort_queryset(queryset, order_by):
    """order_by is an Django ORM order_by argument"""
    if not order_by:
        return queryset

    if need_python_sorting(queryset, order_by):
        # Fallback on pure Python sorting (much slower on large data)

        # The field name can be prefixed by the minus sign and we need to
        # extract this information if we want to sort on simple object
        # attributes (non-model fields)
        if order_by[0] == "-":
            if len(order_by) == 1:
                # Prefix without field name
                raise ValueError

            reverse = True
            name = order_by[1:]
        else:
            reverse = False
            name = order_by
        if hasattr(queryset[0], name):
            return sorted(queryset, key=attrgetter(name), reverse=reverse)
        else:
            raise AttributeError
    else:
        return queryset.order_by(order_by)
