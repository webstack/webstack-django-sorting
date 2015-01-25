from operator import attrgetter


def need_python_sorting(queryset, ordering):
    if ordering.find('__') >= 0:
        # Python can't sort ordering with '__'
        return False

    # Python sorting if not a field
    field = ordering[1:] if ordering[0] == '-' else ordering
    return field not in queryset.model._meta.get_all_field_names()


def sort_queryset(queryset, ordering):
    if ordering:
        if need_python_sorting(queryset, ordering):
            # Fallback on pure Python sorting (much slower on large data)

            # The field name can be prefixed by the minus sign and we need to
            # extract this information if we want to sort on simple object
            # attributes (non-model fields)
            if ordering[0] == '-':
                reverse = True
                name = ordering[1:]
            else:
                reverse = False
                name = ordering
            return sorted(queryset, key=attrgetter(name), reverse=reverse)
        else:
            return queryset.order_by(ordering)
    else:
        return queryset
