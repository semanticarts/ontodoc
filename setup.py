#!/usr/bin/env python

PROJECT = 'ontodoc'

# Change docs/sphinx/conf.py too!
VERSION = '0.01'

from setuptools import setup, find_packages

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(

    name = PROJECT,
    version = VERSION,

    description = 'Generate static ontology documentation from OWL files',
    long_description = long_description,

    author = 'Scott Ogle',
    author_email = 'scott@semanticarts.com',

    # url = 'https://github.com/dreamhost/cliff',
    # download_url = 'https://github.com/dreamhost/cliff/tarball/master',


    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms = ['Any'],

    scripts = [],

    provides = [],
    install_requires = [
        'cliff',
        'sass',
        'jinja2',
        'PyYAML',
        'rdflib'
    ],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'ontodoc = onntodoc.main:main'
        ],
        'ontodoc': [
            'new = ontodoc.create:Create',
            'ontodoc = ginger.build:compile'
        ]
    },


    zip_safe=False,
)
