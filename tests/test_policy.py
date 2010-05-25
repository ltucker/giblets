from helpers import *

def test_blacklist():
    clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements
    from giblets.policy import Blacklist

    class ICog(ExtensionInterface):
        pass
        
    class Widget(Component):
        cogs = ExtensionPoint(ICog)
     
    class GoodCog(Component):
        implements(ICog)
        
    class BadCog(Component):
        implements(ICog)
        
    # first no restrtictions, both should show up
    policy = Blacklist()
    
    mgr = ComponentManager()
    mgr.restrict(policy)
    widget = Widget(mgr)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(1, BadCog, widget.cogs)
    
    policy.disable_component(BadCog)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    # re-enable
    policy.enable_component(BadCog)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(1, BadCog, widget.cogs)

    policy.disable_component('tests.test_policy.BadCog')
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    policy.enable_component('tests.test_policy.BadCog')
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(1, BadCog, widget.cogs)


def test_whitelist():
    clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements
    from giblets.policy import Whitelist
    
    class ICog(ExtensionInterface):
        pass

    class Widget(Component):
        cogs = ExtensionPoint(ICog)

    class GoodCog(Component):
        implements(ICog)

    class BadCog(Component):
        implements(ICog)

    
    policy = Whitelist()
    mgr = ComponentManager()
    mgr.restrict(policy)
    
    # first nothing specified, nothing should show up
    widget = Widget(mgr)
    assert has_exactly(0, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    # enable only the GoodCog
    policy.enable_component(GoodCog)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    # re-disable, should show nothing again
    policy.disable_component(GoodCog)
    assert has_exactly(0, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    # try enable by name...
    policy.enable_component('tests.test_policy.GoodCog')
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    policy.disable_component('tests.test_policy.GoodCog')
    assert has_exactly(0, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)


def test_patterns():
    clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements
    from giblets.policy import Patterns

    class ICog(ExtensionInterface):
        pass

    class Widget(Component):
        cogs = ExtensionPoint(ICog)

    class GoodCog(Component):
        implements(ICog)

    class BadCog(Component):
        implements(ICog)

    policy = Patterns()
    mgr = ComponentManager()
    mgr.restrict(policy)
    widget = Widget(mgr)

    # to start with, everything is disabled...
    assert has_exactly(0, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

    # easy to enable everything...
    policy.append_pattern('*', enable=True)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(1, BadCog, widget.cogs)

    # now just disable the bad one
    pat = policy.build_pattern('tests.test_policy.BadCog', enable=False)
    policy.patterns.insert(0, pat)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)
    
    # disable all the test core components...
    pat = policy.build_pattern('tests.test_policy.*', enable=False)
    policy.patterns.insert(0, pat)
    assert has_exactly(0, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)
