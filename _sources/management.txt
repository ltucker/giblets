===========================
Component Management
===========================

Giblets provides a fairly flexible system for managing which components are enabled in the case that there are more Components available in the environment than should be active in your application or the current context.  If the built-in options are not enough, it's cinch to write your own policy.

By default, all discovered Components are enabled and will appear in all relevant ExtensionPoints.

Components can be refined by applying a restriction policy to the ComponentManager via the ``restrict`` method.  The ComponentManager will delegate ``is_component_enabled`` to the currently set policy.  There are 3 built-in types of policies which can be found in the ``giblets.policy`` module.


Blacklist
-------------------------

All Components are enabled except those explicitly blacklisted by this policy.  Use disable_component and enable_component to add and remove items from the blacklist.


Whitelist
-------------------------

All Components are disabled except those explicitly whitelisted by this policy.  Use enable_component and disable_component to add and remove items from the whitelist.

Patterns
-------------------------

Components are enabled or disabled based on the first matching pattern in a list of wildcard patterns.
If no pattern matches, the Component is disabled.

Example
-------

    A ``Widget`` ``Component`` calls ``turn`` on all things that implement ``ICog`` when ``activate`` is called.

    >>> from giblets import *
    >>>
    >>> class ICog(ExtensionInterface):
    ...     def turn():
    ...         """perform cog action"""
    ...
    >>> class Widget(Component):
    ...     cogs = ExtensionPoint(ICog)
    ...     def activate(self):
    ...         for cog in self.cogs:
    ...             cog.turn()
    ...
    >>> class GoodCog(Component):
    ...     "Well made cog"
    ...     implements(ICog)
    ...     def turn(self):
    ...         print 'clink clink'
    ...
    >>> class CheapCog(Component):
    ...     "Evil Exception raising cog"
    ...     implements(ICog)
    ...     def turn(self):
    ...         raise Exception('CLANG CLANG')
    ...
    
    Nuts. Our ``Widget`` is ready for action, but the ``CheapCog`` is messing 
    everything up. 
    
    >>> mgr = ComponentManager()
    >>> widget = Widget(mgr)
    >>> widget.activate()
    ...
    Traceback (most recent call last):
    ...
    Exception: CLANG CLANG
    
    Let's blacklist it, and try again.
    
    >>> from giblets.policy import Blacklist
    >>> blacklist = Blacklist()
    >>> blacklist.disable_component(CheapCog)
    >>> mgr.restrict(blacklist)
    >>> widget.activate()
    clink clink
    
    That's what I like to hear.