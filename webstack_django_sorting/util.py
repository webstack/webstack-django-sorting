# coding: utf-8

def get_sort_field(request):
    """
    Retrieve field used for sorting a queryset

    :param request: HTTP request
    :return: the sorted field name, prefixed with "-" if ordering is descending
    """
    sort_direction = request.GET.get('dir')
    field_name = (request.GET.get('sort') or '') if sort_direction else ''
    sort_sign = '-' if sort_direction == 'desc' else ''
    result_field = "{sign}{field}".format(sign=sort_sign, field=field_name)
    return result_field
