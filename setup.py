from setuptools import setup, find_packages

version = '0.2'

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
    author='stephane',
    author_email='stephane.raimbault@gmail.com',
    url='http://github.com/stephane/django-sorting/tree/master',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
