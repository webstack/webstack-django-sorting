# -*- coding: utf-8 -*-
#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.2'

setup(
    name='django-sorting',
    version=version,
    description="Like ericflo's django pagination, but this one does the sorting! Used with ericflo's pagination, displaying tabular paginated and sortable data is very easy",
    long_description=open('README.rst').read(),
    author='Stéphane Raimbault',
    author_email='stephane.raimbault@gmail.com',
    url='http://github.com/stephane/django-sorting/',
    packages=['django_sorting'],
    package_dir={'django_sorting': 'django_sorting'},
    include_package_data=True,
    zip_safe=False,
    keywords='sorting,pagination,django',
    license='BSD',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
