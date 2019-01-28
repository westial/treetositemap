#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='treetositemap',
      version='0.1.0b6',
      description='Command line tool that automates the creation of sitemap '
                  'resources and recursively indexes large amount of filtered '
                  'files and directories.',
      author='Jaume Mila',
      author_email='jaume@westial.com',
      packages=find_packages(),
      entry_points={
          "console_scripts": ['treetositemap = treetositemap.__main__:main']
      },
      tests_require=['behave']
)
