How to use webstack-django-sorting
----------------------------------

``webstack-django-sorting`` allows for easy sorting, and sorting links
generation without modifying your views. It is the perfect companion of
linaro-django-pagination",

There are really 5 steps to setting it up with your projects.

1. List this application in the ``INSTALLED_APPS`` portion of your settings
   file.  Your settings file might look something like::

       INSTALLED_APPS = (
           # ...
           'webstack_django_sorting',
       )

2. Install the sorting middleware. Your settings file might look something
   like::

       MIDDLEWARE_CLASSES = (
           # ...
           'webstack_django_sorting.middleware.SortingMiddleware',
       )

3. If it's not already added in your setup, add the 'request' context processor::

       TEMPLATE_CONTEXT_PROCESSORS = (
           'django.contrib.auth.context_processors.auth',
           'django.core.context_processors.debug',
           'django.core.context_processors.i18n',
           'django.core.context_processors.media',
           'django.core.context_processors.static',
           'django.core.context_processors.tz',
           'django.core.context_processors.request',
           'django.contrib.messages.context_processors.messages',
       )

   This example comes from Django 1.6, take care to check against your Django
   version which context processors are supported (see ``global_settings.py``
   file of your Django installation).

4. Add this line at the top of your template to load the sorting tags::

       {% load sorting_tags %}

5. Decide on a variable that you would like to sort, and use the
   autosort tag on that variable before iterating over it::

       {% autosort object_list %}

6. Now, you want to display different headers with links to sort
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
