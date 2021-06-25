#!/usr/bin/env python

from setuptools import setup

setup(
    name="hyperflask",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "hyperflask/_version.py",
        "fallback_version": "0.0.0",
    },
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    description="Flask wrapper to encourage use of REST architectural style and Hypermedia.",
    url="http://github.com/avengerpenguin/hyperflask",
    install_requires=[
        "flask",
        "rdflib",
        "requests",
        "flask_rdf",
        "laconia",
        "sqlalchemy",
    ],
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    extras_require={
        "test": ["pytest", "httpretty"],
    },
    packages=["hyperflask"],
)
