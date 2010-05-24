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

from giblets.core import Component, implements
from tests.test_search import TestPathInterface

class TestPathPlugin1(Component):
    implements(TestPathInterface)

class TestPathPlugin2(Component):
    implements(TestPathInterface)