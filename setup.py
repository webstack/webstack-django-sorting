from setuptools import setup, find_packages

version = '0.1'

setup(
    name='django-sorting',
    version=version,
    description="Like ericflo's django pagination, but this one does the sorting! used with ericflo's pagination, displaying tabular paginated and sortable data is very easy",
    long_description=open('README.rst').read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='sorting,pagination,django',
    author='directeur',
    url='http://github.com/directeur/django-sorting/tree/master',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
