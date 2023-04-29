#!/usr/bin/env python3
"""
Holly
=====

A blog-engine plugin for Ark.

"""

from setuptools import setup

setup(
    name = 'holly',
    version = '2.0.0',
    py_modules = ['holly'],
    author = 'Darren Mulholland',
    url = 'https://github.com/dmulholl/holly',
    license = 'Public Domain',
    description = (
        'A blog-engine plugin for Ark.'
    ),
    long_description = __doc__,
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: Public Domain',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
