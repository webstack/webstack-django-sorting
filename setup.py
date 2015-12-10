# -*- coding: utf-8 -*-
#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '0.4.3'

setup(
    name='webstack-django-sorting',
    version=__version__,
    description="Easy sorting of tables with Django",
    long_description=open('README.rst').read(),
    author='Stéphane Raimbault',
    author_email='stephane.raimbault@webstack.fr',
    url='http://github.com/webstack/webstack-django-sorting/',
    packages=[
        'webstack_django_sorting',
        'webstack_django_sorting.templatetags',
    ],
    package_dir={'webstack_django_sorting': 'webstack_django_sorting'},
    include_package_data=True,
    zip_safe=False,
    keywords='sorting,pagination,django',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
