from django.conf import settings

# HTML entities for sort indicators (default)
DEFAULT_SORT_UP = getattr(settings, "DEFAULT_SORT_UP", " &uarr;")
DEFAULT_SORT_DOWN = getattr(settings, "DEFAULT_SORT_DOWN", " &darr;")

# CSS class-based sort indicators (alternative to HTML entities)
# When set, these CSS classes are added to the anchor tag instead of using icons
# Example: SORTING_CSS_CLASS_ASC = "sorted-asc" produces <a class="sorted-asc" ...>
SORTING_CSS_CLASS_ASC = getattr(settings, "SORTING_CSS_CLASS_ASC", "")
SORTING_CSS_CLASS_DESC = getattr(settings, "SORTING_CSS_CLASS_DESC", "")

INVALID_FIELD_RAISES_404 = getattr(settings, "SORTING_INVALID_FIELD_RAISES_404", False)
