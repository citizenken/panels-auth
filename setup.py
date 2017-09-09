#!/usr/bin/env python

from distutils.core import setup

setup(name='panels-oauth',
      version='1.0',
      description='Python Distribution Utilities',
      author='Ken Petti',
      author_email='kennethpetti@gmail.com',
      install_requires=[
          'Flask',
          'Flask-Dance',
          'oauth2client'
      ],
      dependency_links=[
            'https://github.com/citizenken/flask-dance/tarball/master#egg=Flask-Dance-0.10.2'
      ]
      )
