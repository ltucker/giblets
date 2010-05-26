==========================
Components
==========================


Components and Managers
========================

A ``Component`` is a singleton object that provides some concrete functionality to your application.  You can retrieve a Component similarly to constructing an object, but you will always receive the same object in any given context.  Components are constructed with a ``ComponentManager`` which handles things like what Components are enabled and disabled and making sure that only one instance of each Component is created.

>>> from giblets import Component, ComponentManager
>>>
>>> mgr = ComponentManager()
>>>
>>> class AuthenticationService(Component):
...    def authenticate(self, username, password):
...       if username == password:
...           return True
...       return False
...
>>> auth = AuthenticationService(mgr)
>>> auth.authenticate('joe', 'joe')
True

You will get the same object if you ask for the Component again:

>>> id(auth) == id(AuthenticationService(mgr))
True

One is often enough, but technically speaking, Components are only singletons with respect to the  ``ComponentManager`` they are requested with.  It may be reasonable in some circumstances to maintain multiple non-interacting contexts within a single application.

>>> mgr2 = ComponentManager()
>>> id(auth) == id(AuthenticationService(mgr2))
False

Extending Components
====================

Any ``Component`` can declare an ``ExtensionPoint`` to indicate a particular area where it can be extended by other Components.  Each ExtensionPoint has an associated ``ExtensionInterface`` describing the expectations for extending functionality.

    >>> from giblets import ExtensionPoint, ExtensionInterface
    >>>
    >>> class ITool(ExtensionInterface):
    ...    def apply(canvas, x, y): pass
    ...
    >>> class ToolBox(Component):
    ...    tools = ExtensionPoint(ITool)
    ...
    >>> tool_box = ToolBox(mgr)

Components can declare that they implement an ExtensionInterface using ``implements``.  Any component declaring to implement an ExtensionInterface will automatically appear 'in' corresponding ExtensionPoints.  The ExtensionPoint behaves similarly to a list:

    >>> from giblets import implements
    >>>
    >>> class EraserTool(Component):
    ...    implements(ITool)
    ...    def apply(canvas, x, y): pass # erase...
    ...
    >>> tool_box.tools[0] == EraserTool(mgr)
    True
    

Any Component may declare as many ExtensionPoints as needed, and since things that implement ExtensionInterfaces are also Components, extensions can also have their own ExtensionPoints.

    >>> class IBrushShape(ExtensionInterface):
    ...    pass
    ...
    >>> class PaintBrush(Component):
    ...     implements(ITool)
    ...     shapes = ExtensionPoint(IBrushShape)
    ...     def apply(canvas, x, y): pass # paint at x,y
    ...
    >>> class RoundBrush(Component):
    ...     implements(IBrushShape)
    ...
    >>> tool_box.tools[1].shapes[0] == RoundBrush(mgr)
    True