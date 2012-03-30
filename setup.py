##############################################################################
#
# Copyright (c) 2008 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

__version__ = '0.6.3'

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

if sys.version_info >= (2, 6): #pragma NO COVER Python >= 2.6
    requires = [
        'setuptools',
        'ZODB3',
        'zope.component',
        'zope.interface',
        ]
else: #pragma NO COVER Python < 2.6
    requires = [
        'setuptools',
        'ZODB3<3.10dev',
        'zope.component<3.11dev',
        'zope.interface<3.8dev',
        ]

tests_require = ['Sphinx', 'repoze.sphinx.autointerface', 'zope.testing']

testing_extras = ['nose', 'coverage']

setup(name='repoze.folder',
      version=__version__,
      description='A ZODB folder implementation with object events',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        ],
      keywords='web wsgi zope',
      author="Agendaless Consulting",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      install_requires= requires,
      tests_require = requires + tests_require,
      test_suite="repoze.folder",
      entry_points = """\
      """,
      extras_require = {
        'testing':  requires + tests_require + testing_extras,
      }
)
