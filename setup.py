# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 Luke Tucker
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: Luke Tucker <voxluci@gmail.com>
#

from setuptools import setup, find_packages

version = "0.2.1"

long_description = """
Giblets is a simple plugin system based on the component architecture of 
`Trac <http://trac.edgewall.org>`_.
In a nutshell, giblets allows you to declare interfaces and discover components
that implement them without coupling.

Giblets also includes plugin discovery based on file paths or entry points along with 
flexible means to manage which components are enabled or disabled in your application.

The full documenation for giblets is available at 
`http://ltucker.github.com/giblets <http://ltucker.github.com/giblets>`_.

Installation
=============

To install::

    $ pip install giblets

or::
    
    $ easy_install giblets

You can also install the current 
`development version <http://github.com/ltucker/giblets/tarball/master#egg=giblets-dev>`_ 
of giblets with ``pip install giblets==dev`` or ``easy_install giblets==dev`` 
"""

setup(
    name='giblets',
    version=version,
    description="A simple plugin system based on the component architecture of Trac.",
    long_description=long_description,
    license="BSD",
    author="Luke Tucker",
    author_email="voxluci@gmail.com",
    url="http://github.com/ltucker/giblets",
    install_requires=[
        "zope.interface",
    ],
    dependency_links=[
    ],
    packages=find_packages(),
    namespace_packages=[],
    include_package_data=True,
    test_suite = 'nose.collector',
    entry_points="""
    [giblets_load_from_entry_point_test]
    mod1 = tests.test_plugin_egg.eggmod1
    mod2 = tests.test_plugin_egg.eggmod2
    """,
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Topic :: Software Development'
    ],
    keywords = "plugins components",
)
