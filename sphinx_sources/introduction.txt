==================
Introduction
==================

Giblets provides you with a few basic building blocks that help you add a rich set of interacting plugins to your application.  ``ExtensionInterfaces`` allow you to declare a named set of requirements, and to declare fulfillment of those requirements. ``ExtensionPoints`` allow you to use interfaces to declare well defined areas to extend functionality, and to gather up the things providing the functionality (implementing the interfaces).  The 'things' that can extend and be extended are ``Components`` and the whole mess is managed by a ``ComponentManager``.

Read through the example below to see how you might use these in practice.

Although giblets is slightly different, 
`Trac's documentation <http://trac.edgewall.org/wiki/TracDev/ComponentArchitecture>`_ also provides a thorough conceptual overview. 


Example 
=======
    In this example we create a "tool box" that can have a pluggable set of "tools".
    
    First, we declare what we mean by a tool using an interface.  In giblets parlance 
    this is called an ``ExtensionInterface``.  For simplicity's sake, we'll just say that
    every tool has a name.
    
    >>> from giblets import ExtensionInterface
    >>>
    >>> class ITool(ExtensionInterface):
    ...    def name():
    ...       """the name of this tool."""
    ...

    Great. Now we declare our "tool box".  Everything concrete in giblets is a
    subclass of ``Component``.  This particular Component is one that can be 
    extended with ITools.  To express this, we declare an ExtensionPoint.
     
    >>> from giblets import Component, ExtensionPoint
    >>>
    >>> class ToolBox(Component):
    ...     tools = ExtensionPoint(ITool)
    ...
    
    Nice. Now we declare a couple of tools to round things out.  These will also be 
    Components, but they will declare that they implement the ITool interface using
    the ``implements`` statement and actually implement the interface by declaring a 
    name.
    
    >>> from giblets import implements
    >>>
    >>> class Hammer(Component):
    ...     implements(ITool)
    ...     def name(self):
    ...         return 'Hammer'
    ...
    >>> class Saw(Component):
    ...     implements(ITool) 
    ...     def name(self):
    ...        return 'Saw'
    ...
    
    Phew. okay, now things are looking really amazing. One last thing, all Components are 
    managed by a ``ComponentManager``.  You get the same Component back for a given
    ComponentManager whenever you ask for it.  Let's see how that works.
    
    >>> from giblets import ComponentManager
    >>> mgr = ComponentManager()
    >>>
    >>> toolbox = ToolBox(mgr)
    
    Easy.  Now lets look at the ToolBox's tools.  It's just a list of Components as 
    it turns out, each implementing the ITool interface: 
    
    >>> for tool in toolbox.tools:
    ...     print tool.name()
    Hammer
    Saw

