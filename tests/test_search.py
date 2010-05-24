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

from giblets import ExtensionInterface

class TestPathInterface(ExtensionInterface):
    pass

class TestEggInterface(ExtensionInterface):
    pass

def test_load_from_path():
    from giblets.core import ComponentManager, Component, ExtensionPoint
    from giblets.search import find_plugins_in_path
    
    class PluginFinder(Component):
        found_plugins = ExtensionPoint(TestPathInterface)

    mgr = ComponentManager()
    pf = PluginFinder(mgr)
    
    # to start with, nothing should be found    
    assert len(pf.found_plugins) == 0
    
    find_plugins_in_path('test_plugin_path')

    expected_plugins = ['TestPathPlugin1', 'TestPathPlugin2', 'TestPathPlugin3']
    got_plugins = set()

    assert len(pf.found_plugins) == len(expected_plugins)    
    for plugin in pf.found_plugins:
        plugin_name = plugin.__class__.__name__
        assert plugin_name in expected_plugins
        got_plugins.add(plugin_name)
    for plugin_name in expected_plugins:
        assert plugin_name in got_plugins
    
def test_load_from_entry_point():
    from giblets.core import ComponentManager, Component, ExtensionPoint
    from giblets.search import find_plugins_by_entry_point
    
    class PluginFinder(Component):
        found_plugins = ExtensionPoint(TestEggInterface)

    mgr = ComponentManager()
    pf = PluginFinder(mgr)
    
    # to start with, nothing should be found    
    assert len(pf.found_plugins) == 0
    
    find_plugins_by_entry_point('giblets_load_from_entry_point_test')

    expected_plugins = ['TestEggPlugin1', 'TestEggPlugin2', 'TestEggPlugin3']
    got_plugins = set()

    assert len(pf.found_plugins) == len(expected_plugins)    
    for plugin in pf.found_plugins:
        plugin_name = plugin.__class__.__name__
        assert plugin_name in expected_plugins
        got_plugins.add(plugin_name)
    for plugin_name in expected_plugins:
        assert plugin_name in got_plugins
    