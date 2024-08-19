from markupsafe import Markup

from . import common


def sorting_anchor(request, field_name, title, default_sort_order="asc"):
    return Markup(common.render_sort_anchor(request, field_name, title, default_sort_order))


def sort_queryset(request, queryset, **context_var):
    order_by = common.get_order_by_from_request(request)
    null_ordering = common.get_null_ordering(request, context_var.get("nulls"))
    return common.sort_queryset(queryset, order_by, null_ordering)
