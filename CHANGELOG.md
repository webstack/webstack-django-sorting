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

v2.3.0
------

- Change target version of Black to Python 3.11
- Fix deprecated `USE_L10N`
- Fix deprecated `assertQuerysetEqual`
- Remove URL list provided by new home page
- Add new home view to list of views
- Fix HTML and add comment in <p>
- Upgrade testproj to Django v5
- Fix self.null_ordering reassignment to avoid modification in template. Thanks
  to @sandre35.

v2.2.1
------

- Minor change to `README.md`

v2.2.0
------

- Update the list of URLs in README of testproj.
- Support Django v4.1
- Rewrite bad comparison of instances against strings
- Add note about settings in README
- Provide 'nulls' examples for Jinja
- Remove useless imports
- Handle invalid values of nulls with 404 setting
- Update tests after API changes (nulls=first|last)
- Adjust URL name of test project
- Add information about test project in main README.md
- Fix format and import ordering
- New way to pass nulls ordering. Thanks to @manderj.

v2.1.1
------

- Fix deprecated import of Markup from jinja2
- Add doc about nulls_first in README and fix typo

v2.1.0
------

- Fix incorrect setup of static files
- tests: serve common templates css through static files. Thanks to @manderj.
- Add sorting by nulls first or last. Thanks to @manderj.

v2.0.3
------

- Add rule for Black in pyproject.toml
- Fix Jinja2 is required (#19)
- Added Django 4.0 support. Thanks to David Smith.

v2.0.2
------

- Fix missing other GET params in anchors
- pip instal -e doesn't work w/o setup.py
- Fix path to jinj2 tags in testproj

v2.0.1
------

- Fix trailing commas in classifiers

v2.0.0
------

Released on February 23th, 2021

- Python v3.6+ only
- Remove support of Django <1.8
- Major cleanup of code
- Jinja2 support
- Merge setup.py and setup.cfg in setup.cfg
- Provide pyproject.toml

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
