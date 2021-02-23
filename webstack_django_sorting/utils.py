from urllib.parse import urlencode

from .settings import SORT_DIRECTIONS


def get_sort_field(request):
    """
    Retrieve field used for sorting a queryset

    :param request: HTTP request
    :return: the sorted field name, prefixed with "-" if ordering is descending
    """
    sort_direction = request.GET.get("dir")
    field_name = (request.GET.get("sort") or "") if sort_direction else ""
    sort_sign = "-" if sort_direction == "desc" else ""
    return f"{sort_sign}{field_name}"


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
