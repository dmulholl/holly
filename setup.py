#!/usr/bin/env python3
"""
Holly
=====

A blog-engine plugin for Ivy.

"""

from setuptools import setup

setup(
    name = 'holly',
    version = '0.2.0',
    py_modules = ['holly'],
    author = 'Darren Mulholland',
    url = 'https://github.com/dmulholl/holly',
    license = 'Public Domain',
    description = (
        'A blog-engine plugin for Ivy.'
    ),
    long_description = __doc__,
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: Public Domain',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
