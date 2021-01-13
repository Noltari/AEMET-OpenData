#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = [x.strip() for x in open(here('requirements.txt')).readlines()]

setup(name='AEMET-OpenData',
      version='0.1.7',
      description='AEMET OpenData Rest API library',
      keywords='aemet',
      author='noltari',
      author_email='noltari@gmail.com',
      url='https://github.com/Noltari/AEMET-OpenData',
      install_requires=requirements,
      license="GPL2",
      zip_safe=False,
      platforms=["any"],
      packages=find_packages(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
      ],
)
