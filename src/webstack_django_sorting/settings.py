from django.conf import settings

DEFAULT_SORT_UP = getattr(settings, "DEFAULT_SORT_UP", " &uarr;")
DEFAULT_SORT_DOWN = getattr(settings, "DEFAULT_SORT_DOWN", " &darr;")
INVALID_FIELD_RAISES_404 = getattr(settings, "SORTING_INVALID_FIELD_RAISES_404", False)