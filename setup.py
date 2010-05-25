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

setup(
    name='giblets',
    version="0.2",
    description="A simple plugin system based on the component architecture of Trac.",
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
)
