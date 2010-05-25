==================================
Interfaces in depth
==================================

Declaring an Interface
=======================

A giblets interface must be a direct or indirect subclass of ``ExtensionInterface``

    >>> from giblets import ExtensionInterface
    >>>
    >>> class IFoo(ExtensionInterface):
    ...     "this works"
    ...

Interface Functions and Attributes
===================================

interfaces can declare expectations of classes that provide an interface by 
declaring stub functions and dummy attributes.  These aren't enforced in any 
way, but help to clearly indicate what is expected to participate.

    >>> from giblets import Attribute
    >>>
    >>> class IBall(ExtensionInterface):
    ...     radius = Attribute('the radius of the ball')
    ...     def bounce():
    ...         "perform the bounce action"


Implementing Interfaces
=========================

    To implement an Extension interface, two things are necessary: the class
    must be a subclass of ``Component`` and the class must include an ``implements`` 
    statement in its declaration listing the interfaces the component provides.

    >>> from giblets import Component, implements
    >>>
    >>> class BaseBall(Component):
    ...     implements(IBall)
    ...     radius = 10
    ...     def bounce(self):
    ...         print 'thunk'
    
    It is fine to implement multiple interfaces:

    >>> class IBodyPart(ExtensionInterface):
    ...     number_per_body = Attribute('how many of these are in a body')
    ...
    >>> class EyeBall(Component):
    ...     implements(IBall, IBodyPart)
    ...     radius = 1
    ...     number_per_body = 2
    ...     def bounce(self):
    ...         print 'squish'
    ...


Inspecting a Component's Interfaces
===================================

    You can walk over the interfaces provided by a Component by using 
    ``implemented_by``. 
    
    >>> from giblets import implemented_by
    >>> for iface in implemented_by(EyeBall):
    ...     print iface.__name__
    IBall
    IBodyPart
    
    You can test whether a Component provides an interface by calling ``is_implemented_by``
    
    >>> from giblets import is_implemented_by
    >>> is_implemented_by(EyeBall, IBall)
    True
    >>> is_implemented_by(EyeBall, IFoo)
    False
    


Inheritance
=====================

    Interfaces can also subclass other interfaces, and things 
    will behave in a predictable way.
    
    
    >>> class IVehicle(ExtensionInterface):
    ...     pass
    ...
    >>> class IFloat(ExtensionInterface):
    ...     pass
    ...
    >>> class IBoat(IVehicle, IFloat):
    ...     pass
    ...
    >>> class Sailboat(Component):
    ...     implements(IBoat)
    ...
    >>> is_implemented_by(Sailboat, IBoat)
    True
    >>> is_implemented_by(Sailboat, IFloat)
    True
    >>> is_implemented_by(Sailboat, IVehicle)
    True
    
    Likewise, you can subclass Components and inherit their interface
    declarations.
    
    >>> class Sloop(Sailboat):
    ...    pass
    ...
    >>> is_implemented_by(Sloop, IBoat)
    True
    >>> is_implemented_by(Sloop, IFloat)
    True
    >>> is_implemented_by(Sloop, IVehicle)
    True

    But in some cases, this may be more than is desired.  In those cases, 
    you can use ``implements_only`` instead of ``implements``
    
    >>> from giblets import implements_only
    >>>
    >>> class SunkenHull(Sailboat):
    ...     implements_only(IVehicle)
    ...
    >>> is_implemented_by(SunkenHull, IBoat)
    False
    >>> is_implemented_by(SunkenHull, IFloat)
    False
    >>> is_implemented_by(SunkenHull, IVehicle)
    True
    
    Be careful though, this does not limit interface inheritance.
    
    >>> class Sunfish(Sailboat):
    ...     implements_only(IBoat)
    ...
    >>> is_implemented_by(Sunfish, IBoat)
    True
    >>> is_implemented_by(Sunfish, IFloat)
    True
    >>> is_implemented_by(Sunfish, IVehicle)
    True
