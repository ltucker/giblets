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

from giblets import Component, implements
from tests.test_search import TestEggInterface

class TestEggPlugin3(Component):
    implements(TestEggInterface)