# coding: utf-8
from operator import attrgetter

from django import template, VERSION as DJANGO_VERSION
from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from ..util import get_sort_field


register = template.Library()

DEFAULT_SORT_UP = getattr(settings, 'DEFAULT_SORT_UP', '&uarr;')
DEFAULT_SORT_DOWN = getattr(settings, 'DEFAULT_SORT_DOWN', '&darr;')
INVALID_FIELD_RAISES_404 = getattr(settings, 'SORTING_INVALID_FIELD_RAISES_404', False)

sort_directions = {
    'asc': {'icon': DEFAULT_SORT_UP, 'inverse': 'desc'},
    'desc': {'icon': DEFAULT_SORT_DOWN, 'inverse': ''},
    '': {'icon': '', 'inverse': 'asc'},
}


def anchor(parser, token):
    """
    Parses a tag that's supposed to be in this format '{% anchor field title %}'
    Title may be a "string", _("trans string"), or variable
    """
    bits = [b for b in token.split_contents()]
    if len(bits) < 2:
        raise template.TemplateSyntaxError("anchor tag takes at least 1 argument.")

    title_is_var = False
    try:
        title = bits[2]
        if title[0] in ('"', "'"):
            if title[0] == title[-1]:
                title = title[1:-1]
            else:
                raise template.TemplateSyntaxError(
                    'anchor tag title must be a "string", _("trans string"), or variable')
        elif title.startswith('_("') or title.startswith("_('"):
            title = _(title[3:-2])
        else:
            title_is_var = True
    except IndexError:
        title = bits[1].capitalize()

    return SortAnchorNode(bits[1].strip(), title.strip(), title_is_var)


class SortAnchorNode(template.Node):
    """
    Renders an <a> HTML tag with a link which href attribute
    includes the field on which we sort and the direction.
    and adds an up or down arrow if the field is the one
    currently being sorted on.

    Eg.
        {% anchor name Name %} generates
        <a href="/the/current/path/?sort=name" title="Name">Name</a>

    """
    def __init__(self, field, title, title_is_var):
        self.field = field
        self.title = title
        self.title_is_var = title_is_var

    def render(self, context):
        if self.title_is_var:
            self.title = context[self.title]
        request = context['request']
        getvars = request.GET.copy()

        if 'sort' in getvars:
            sortby = getvars['sort']
            del getvars['sort']
        else:
            sortby = ''

        if 'dir' in getvars:
            sortdir = sort_directions.get(getvars['dir'], sort_directions[''])
            del getvars['dir']
        else:
            sortdir = sort_directions['']

        if sortby == self.field:
            getvars['dir'] = sortdir['inverse']
            icon = sortdir['icon']
        else:
            getvars['dir'] = 'asc'
            icon = ''

        if getvars['dir'] == '':
            getvars.pop('dir', None)

        if len(getvars.keys()) > 0:
            urlappend = "&%s" % getvars.urlencode()
        else:
            urlappend = ''

        if icon:
            title = "%s %s" % (self.title, icon)
        else:
            title = self.title

        if 'dir' in getvars:
            url = '%s?sort=%s%s' % (request.path, self.field, urlappend)
        else:
            url = '%s%s%s' % (request.path, '?' if urlappend else '', urlappend)
        return '<a href="%s" title="%s">%s</a>' % (url, self.title, title)


def autosort(parser, token):
    bits = [b.strip('"\'') for b in token.split_contents()]
    help_msg = u'autosort tag synopsis: {%% autosort queryset [as '\
        u'context_variable] %%}'
    context_var = None

    # Check if has not required "as new_context_var" part
    if len(bits) == 4 and bits[2] == 'as':
        context_var = bits[3]
        del bits[2:]

    if len(bits) != 2:
        raise template.TemplateSyntaxError(help_msg)

    return SortedDataNode(bits[1], context_var=context_var)


class SortedDataNode(template.Node):
    """
    Automatically sort a queryset with {% autosort queryset %}
    """
    def __init__(self, queryset_var, context_var=None):
        self.queryset_var = template.Variable(queryset_var)
        self.context_var = context_var

    def need_python_sorting(self, queryset, ordering):
        if ordering.find('__') >= 0:
            # Python can't sort ordering with '__'
            return False

        # Python sorting if not a field
        field = ordering[1:] if ordering[0] == '-' else ordering

        if DJANGO_VERSION < (1, 8):
            field_names = queryset.model._meta.get_all_field_names()
        else:
            field_names = [f.name for f in queryset.model._meta.get_fields()]

        return field not in field_names

    def sort_queryset(self, queryset, ordering):
        if not ordering:
            return queryset

        if queryset.exists():
            if self.need_python_sorting(queryset, ordering):
                # Fallback on pure Python sorting (much slower on large data)

                # The field name can be prefixed by the minus sign and we need to
                # extract this information if we want to sort on simple object
                # attributes (non-model fields)
                if ordering[0] == '-':
                    if len(ordering) == 1:
                        # Prefix without field name
                        raise template.TemplateSyntaxError

                    reverse = True
                    name = ordering[1:]
                else:
                    reverse = False
                    name = ordering
                if hasattr(queryset[0], name):
                    return sorted(queryset, key=attrgetter(name), reverse=reverse)
                else:
                    raise AttributeError()
            else:
                return queryset.order_by(ordering)

    def render(self, context):
        if self.context_var is not None:
            key = self.context_var
        else:
            key = self.queryset_var.var

        queryset = self.queryset_var.resolve(context)
        ordering = get_sort_field(context['request'])

        try:
            context[key] = self.sort_queryset(queryset, ordering)
        except (template.TemplateSyntaxError, AttributeError):
            if INVALID_FIELD_RAISES_404:
                raise Http404(
                    'Invalid field sorting. If DEBUG were set to '
                    'False, an HTTP 404 page would have been shown instead.')
            context[key] = queryset

        return u''


anchor = register.tag(anchor)
autosort = register.tag(autosort)
