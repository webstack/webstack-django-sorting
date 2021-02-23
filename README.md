# webstack-django-sorting

## What?

`webstack-django-sorting` is a Django app which allows for easy sorting of
data tables. You don't need to change anything to your views to use it. It
provides sorting links for table headers. It is the perfect companion of
[django-pagination](https://github.com/zyga/django-pagination).

There are other powerful projects to sort tables such as
[django-tables2](https://django-tables2.readthedocs.io/) but I don't like the
high level `render_table` tag because it requires to define the CSS in
`Table` classes or to write custom templates.

A demonstration of the features is provided in `testproj` directory.

## Features

- Django or Jinja2 templates
- Django ORM or Python sorting
- Switches between ascending, descending, and no sorting
- Provides links to sort on different criterions
- Visual feedback on applied ordering
- Supports 3.6+
- Supports translation of link titles

To upgrade to `webstack-django-sorting` v1.0.0+, you must remove the old middleware
`webstack_django_sorting.middleware.SortingMiddleware` from `MIDDLEWARE_CLASSES` list.

## How to use it in your project

The provide is available on PyPI:

    pip install webstack_django_sorting

The project provides examples of integration with Django and Jinja2 templates.

## For Django templates

1. Add the application to the `INSTALLED_APPS` list:

    ```python
       INSTALLED_APPS = [
           # ...
           'webstack_django_sorting',
       ]
    ```

2. Check the request context processor is loaded in `TEMPLATES` options:

    ```python
       TEMPLATES = [
           {
               'BACKEND': 'django.template.backends.django.DjangoTemplates',
               'DIRS': [],
               'APP_DIRS': True,
               'OPTIONS': {
                   'context_processors': [
                       # ...
                       'django.template.context_processors.request',
                       # ...
                   ],
               },
           },
       ]
    ```

3. Add this line at the top of your template to load the sorting tags:

       {% load sorting_tags %}

4. Decide on a variable that you would like to sort, and use the
   autosort tag on that variable before iterating over it:

       {% autosort object_list %}

5. Now, you want to display different headers with links to sort
   your objects_list:

    ```html
        <tr>
           <th>{% anchor first_name _("Name") %}</th>
           <th>{% anchor creation_date _("Creation") %}</th>
        </tr>
    ```

   The first argument is a field or an attribute of the objects list, and the
   second one (optional) is a title that would be displayed. The previous
   snippet will be rendered like this in French:

    ```html
        <tr>
            <th><a href="/path/to/your/view/?sort=first_name" title="Nom">Nom</a></th>
            <th><a href="/path/to/your/view/?sort=creation_date" title="Création">Création</a></th>
        </tr>
    ```

   If your application doesn't support internationalization, you can use a
   simple `{% anchor first_name Name %}`.

## For Jinja2 templates

1. Define the environment in the `TEMPLATES` options:

    ```python
        TEMPLATES = {
            {
                "BACKEND": "django.template.backends.jinja2.Jinja2",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "environment": "testproj.testapp.jinja2.env.JinjaEnvironment",
                },
            },
        ]
    ````

2. Your environment file should add `sorting_anchor` and `sort_queryset` to globals:

    ```python
    from jinja2.environment import Environment
    from webstack_django_sorting.templatetags.jinja2_globals import sorting_anchor, sort_queryset

    class JinjaEnvironment(Environment):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.globals["sorting_anchor"] = sorting_anchor
            self.globals["sort_queryset"] = sort_queryset
    ```

3. Now, you can generate header links to sort your queryset:

    ```html
        <tr>
           <th>{{ sorting_anchor(request, "created_on", "Date") }}</th>
           <!--...-->
        <tr>
    ```

4. The queryset should be wrapped with `sort_queryset` to use the GET request arguments for sorting:

    ```html
        {% for secret_file in sort_queryset(request, secret_files) %}
        <!--...-->
        {% endfor %}
    ```


That's it!
