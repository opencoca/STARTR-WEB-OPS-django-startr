import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-startr',
    version='0.22',
    packages=['django_startr'],
    include_package_data=True,
    license='BSD License',
    description='Management command that generates views, forms, urls, admin, and templates for models',
    long_description=README,
    url='https://github.com/opencoca/STARTR-WEB-OPS-django-startr',
    author='Alexander Somma',
    author_email='asomma@startr.ca',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='generator generates',
)