#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name="hyperflask",
    version="0.0.0",
    author='Ross Fenning',
    author_email='github@rossfenning.co.uk',
    description='Flask wrapper to encourage use of REST architectural style and Hypermedia.',
    url='http://github.com/avengerpenguin/hyperflask',
    install_requires=[
        'flask', 'rdflib', 'flask_rdf',
        ],
    packages=['hyperflask'],
)
