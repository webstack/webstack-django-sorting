def get_field(self):
    try:
        field = self.REQUEST['sort']
    except (KeyError, ValueError, TypeError):
        field = None
    if field:
        return (self.direction == 'desc' and '-' or '') + field
    # No sort key means default sorting
    return ''


def get_direction(self):
    try:
        return self.REQUEST['dir']
    except (KeyError, ValueError, TypeError):
        return 'desc'


class SortingMiddleware(object):
    """
    Inserts a variable representing the field (with direction of sorting)
    onto the request object if it exists in either **GET** or **POST**
    portions of the request.
    """
    def process_request(self, request):
        request.__class__.field = property(get_field)
        request.__class__.direction = property(get_direction)
