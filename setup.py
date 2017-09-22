#!/usr/bin/env python

from distutils.core import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='pyarxiv',
      version='1.0',
      install_requires=requirements,
      description='Python Client Library and CLI client for the ArXiv.org API',
      author='Christoph Ulshoefer',
      author_email='c@culshoefer.com',
      packages=find_packages(),
      url='https://github.com/culshoefer/pyarxiv/',
      test_suite='tests'
      )
