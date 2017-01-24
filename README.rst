webstack-django-sorting
=======================

``webstack-django-sorting`` allows for easy sorting of data tables and it
provides sorting links for table headers. It is the perfect
companion of `django-pagination <https://github.com/zyga/django-pagination>`_.

A demonstration of the features is provided in `testproj` directory.

To upgrade to ``webstack-django-sorting`` v1.0.0+, you must remove the old middleware
``webstack_django_sorting.middleware.SortingMiddleware`` from ``MIDDLEWARE_CLASSES`` list.

How to install it in your project
---------------------------------

The 5 steps to use ``webstack-django-sorting`` in your Django project:

1. Add the application to the ``INSTALLED_APPS`` list::

       INSTALLED_APPS = [
           # ...
           'webstack_django_sorting',
       ]

2. Check the request context processor is loaded in ``TEMPLATES`` options::

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

3. Add this line at the top of your template to load the sorting tags::

       {% load sorting_tags %}

4. Decide on a variable that you would like to sort, and use the
   autosort tag on that variable before iterating over it::

       {% autosort object_list %}

5. Now, you want to display different headers with links to sort
   your objects_list::

       <tr>
           <th>{% anchor first_name _("Name") %}</th>
           <th>{% anchor creation_date _("Creation") %}</th>
       </tr>

   The first argument is a field or an attribute of the objects list, and the
   second one (optional) is a title that would be displayed. The previous
   snippet will be rendered like this in French::

        <tr>
            <th><a href="/path/to/your/view/?sort=first_name" title="Nom">Nom</a></th>
            <th><a href="/path/to/your/view/?sort=creation_date" title="Création">Création</a></th>
        </tr>

   If your application doesn't support internationalization, you can use a
   simple ``{% anchor first_name Name %}``.

That's it!
