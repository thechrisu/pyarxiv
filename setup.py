#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='pyarxiv',
      version='1.0.3',
      install_requires=requirements,
      classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Console'
      ],
      description='Python Client Library and CLI client for the ArXiv.org API',
      long_description="See source on GitHub: https://github.com/culshoefer/pyarxiv\n\n" + readme,
      author='Christoph Ulshoefer',
      license='MIT',
      author_email='c@culshoefer.com',
      packages=['pyarxiv'],
      url='https://github.com/culshoefer/pyarxiv/',
      scripts=['scripts/pyarxiv-cli'],
      test_suite='tests'
      )
