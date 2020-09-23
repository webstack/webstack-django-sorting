webstack-django-sorting
=======================

What?
-----

`webstack-django-sorting` is a Django app which allows for easy sorting of
data tables. You don't need to change anything to your views to use it. It
provides sorting links for table headers. It is the perfect companion of
[django-pagination](https://github.com/zyga/django-pagination).

A demonstration of the features is provided in `testproj` directory.

Features
--------

- Django ORM or Python sorting
- Switches between ascending, descending, and no sorting
- Provides links to sort on different criterions
- Visual feedback on applied ordering
- Supports Python 2.7, 3.5+
- Supports translation of link titles

Upgrade from v0.5.0
-------------------

To upgrade to `webstack-django-sorting` v1.0.0+, you must remove the old middleware
`webstack_django_sorting.middleware.SortingMiddleware` from `MIDDLEWARE_CLASSES` list.

How to use it in your project
---------------------------------

1. `pip install webstack_django_sorting`

2. Add the application to the `INSTALLED_APPS` list:

    ```python
       INSTALLED_APPS = [
           # ...
           'webstack_django_sorting',
       ]
    ```

3. Check the request context processor is loaded in `TEMPLATES` options:

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

4. Add this line at the top of your template to load the sorting tags:

       {% load sorting_tags %}

5. Decide on a variable that you would like to sort, and use the
   autosort tag on that variable before iterating over it:

       {% autosort object_list %}

6. Now, you want to display different headers with links to sort
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

That's it!
