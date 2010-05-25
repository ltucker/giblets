import fnmatch
import re

from giblets.core import _component_id

__all__ = ['Blacklist', 'Whitelist', 'Patterns']

class Blacklist(object):
    """
    policy that activates all Components that
    have not been specifically disabled.
    """

    def __init__(self):
        self.blacklist = set()

    def enable_component(self, component):
        """
        Allow the component specified to be activated
        for this ComponentManager.

        component may be a full class name string 'foo.bar.Quux' 
        a Component type or an instance of a Component.
        """
        try:
            self.blacklist.remove(_component_id(component))
        except KeyError:
            pass

    def disable_component(self, component):
        """
        Do not allow the component specified to be activated
        for this ComponentManager.

        component may be a full class name string 'foo.bar.Quux' 
        a Component type or an instance of a Component.
        """
        component_id = _component_id(component)
        self.blacklist.add(component_id)

    def is_component_enabled(self, component):
        """
        returns True unless the component specified 
        has been disabled.
        """
        if _component_id(component) in self.blacklist:
            return False
        return True

class Whitelist(object):
    """
    Policy that activates only Components
    that have been specifically enabled.
    """

    def __init__(self):
        self.whitelist = set()

    def enable_component(self, component):
        """
        Allow the component specified to be activated
        for this ComponentManager.

        component may be a full class name string 'foo.bar.Quux' 
        a Component type or an instance of a Component.
        """
        self.whitelist.add(_component_id(component))

    def disable_component(self, component):
        """
        Do not allow the component specified to be activated
        for this ComponentManager.

        component may be a full class name string 'foo.bar.Quux' 
        a Component type or an instance of a Component.
        """
        try:
            self.whitelist.remove(_component_id(component))
        except KeyError:
            pass

    def is_component_enabled(self, component):
        """
        returns False unless the component specified has been 
        enabled.
        """
        return _component_id(component) in self.whitelist

class Patterns(object):
    """
    A policy which enables and disables components
    based on an ordered list of wildcard patterns like foo.bar.* 
    etc. First match is taken. 
    """
    
    def __init__(self):
        self.patterns = []

    def build_pattern(self, pattern, enable):
        """
        create an entry suitable for insertion into the 
        patterns list of this manager. 
        
        If pattern is a string, it is 
        treated as a wildcard patten like foo.bar.*
        
        Otherwise, it is assumed pattern is a compiled
        regular expression.
        
        eg: 
        pat = mgr.build_pattern('foo.*', True)
        mgr.patterns.insert(0, pat)
        """
        if isinstance(pattern, basestring):
            pattern = re.compile(fnmatch.translate(pattern))
        return (pattern, enable)

    def append_pattern(self, pattern, enable):
        """
        helper to add a pattern to the end of the 
        list of patterns.
        """
        pat = self.build_pattern(pattern, enable)
        self.patterns.append(pat)

    def is_component_enabled(self, component):
        enabled = False
        comp_id = _component_id(component)
        for (pat, state) in self.patterns:
            if pat.match(comp_id) is not None:
                enabled = state
                break
        return enabled

