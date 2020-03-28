#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='msw',
    version='0.2',
    description='Microservice Worker',
    author='Ethan Chapman',
    author_email='me@ethanchap.com',
    packages=['msw'],
    install_requires=[
        'kafka-python==2.0.1',
    ]
)
