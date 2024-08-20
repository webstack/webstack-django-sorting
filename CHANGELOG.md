Webstack-django-sorting Changelog
=================================

v3.0.0
------

Released on August 19th, 2024

- New optional paramater to set default sort order on first click of a column.
  Thanks to @RhinoW.
- Migrate test project to rye

v2.4.0
------

- Migrate library to rye

v2.3.1
------

- Fix release v2.3.0 on the supported Django version (v5).

v2.3.0
------

- Support Django 5.0
- Fix nulls=last persistency in template (#26). Thanks @sandre35.
- Migrate `testproj` to Django v5.0 (fix deprecated)
- Add home view to `testproj` to list all views
- Fix HTML of test views

v2.2.1
------

- Minor change to `README.md`

v2.2.0
------

No build.

- Breaking change, `nulls_first=True` and `nulls_last=True` are replaced by `nulls=first | last`.
  Thanks to @manderj.
- Support of Django 4.1
- Handle setting to raise 404 on invalid values for new 'nulls' option
- Add more examples for Jinja
- Various cleanup

v2.1.1
------

- Fix deprecated import of Markup from Jinja2

v2.1.0
------

- Add sorting by nulls first or last by @manderj.

v2.0.3
------

- Added Django 4.0 support. Thanks to David Smith.
- Fix Jinja2 is required (#19)

v2.0.2
------

- Fix missing other GET params in anchors
- Fix path to jinja2 tags in testproj
- Fix trailing commas in classifiers

v2.0.1
------

- Fix trailing commas in classifiers (`setup.cfg`).

v2.0.0
------

Released on February 23th, 2021

- **Add Jinja2 suppor**t \o/
- Modern Python packaging
- Add note about django-tables2 in README
- Add documentation for Jinja2
- Include the space before the icon in settings
- Simpler code to render anchor
- Rename 'inverse' key to 'next' in SORT_DIRECTIONS
- Move settings to one upper level
- Use f-strings
- Fix error handling in queryset sorting
- Move sort_directions dict into dedicated file
- Regenerate test project with Django 3.1
- Remove support of Python 2 and upgrade to Django >=3.0
- Various cleanups

v1.0.2
------

Released on September 23th 2020

- Fix cache issue with translatable anchors. Thanks Kim Wong.
- Updated README.md

v1.0.1
------

Released on March 1st 2017

- Improved README
- Don't return None when queryset is empty (closes #8)

v1.0.0
------

Released on January 24th 2017

- Now switching between ascending, descending, and no sorting
- Removed webstack_django_sorting.middleware.SortingMiddleware
- Fixed sorting on edge cases
- Django 1.10 support
- Improved Python 3 support
- Add first tests

v0.5.0
------

Released on January 3rd 2017

- Restore compatibility with Django v1.8 and lower
- Fix reading of README.rst with Python 3
- Cleanup in test project

v0.4.3
------

Released on December 10th 2016

- Compatibility with Django v1.9
- Better MANIFEST.in
