from jinja2 import Markup

from . import common


def sorting_anchor(request, field_name, title):
    return Markup(common.render_sort_anchor(request, field_name, title))


def sort_queryset(request, queryset):
    order_by = common.get_order_by_from_request(request)
    return common.sort_queryset(queryset, order_by)
