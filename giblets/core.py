# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2009 Edgewall Software
# Copyright (C) 2003-2004 Jonas Borgström <jonas@edgewall.com>
# Copyright (C) 2004-2005 Christopher Lenz <cmlenz@gmx.de>
# All rights reserved.
#
# This software is licensed as described in the file COPYING.trac, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.
#
# Author: Luke Tucker <voxluci@gmail.com>
#         Jonas Borgström <jonas@edgewall.com>
#         Christopher Lenz <cmlenz@gmx.de>


from zope import interface as zi
from zope.interface import Attribute, Interface
from zope.interface.advice import addClassAdvisor

__all__ = ['Attribute', 'Component', 'ComponentManager', 'ExtensionPoint', 'ExtensionInterface', 
           'implements', 'implements_only', 'implemented_by', 'is_implemented_by', 
           'ExtensionError']

class ExtensionError(Exception):
    """Exception for extension related errors."""

class ExtensionInterface(Interface):
    """Marker class for extension interfaces and extensions"""

class ExtensionPoint(property):
    """Marker class for extension points in components."""

    def __init__(self, interface):
        """Create the extension point.
        
        @param interface: the `ExtensionInterface` subclass that defines the protocol
            for the extension point
        """
        property.__init__(self, self.extensions)
        self.interface = interface
        self.__doc__ = 'List of components that implement `%s`' % \
                       self.interface.__name__

    def extensions(self, component):
        """Return a list of components that declare they implement the extension
        point interface.
        """
        extensions = ComponentMeta._registry.get(self.interface, [])
        return filter(None, [component.compmgr[cls] for cls in extensions])

    def __repr__(self):
        """Return a textual representation of the extension point."""
        return '<ExtensionPoint %s>' % self.interface.__name__


class ComponentMeta(type):
    """Meta class for components.
    
    Takes care of component and extension point registration.
    """
    _components = []
    _registry = {}

    def __new__(cls, name, bases, d):
        """Create the component class."""

        new_class = type.__new__(cls, name, bases, d)
        if name == 'Component':
            # Don't put the Component base class in the registry
            return new_class

        # Only override __init__ for Components not inheriting ComponentManager
        if not any(issubclass(x, ComponentManager) for x in bases):
            # Allow components to have a no-argument initializer so that
            # they don't need to worry about accepting the component manager
            # as argument and invoking the super-class initializer
            init = d.get('__init__')
            if not init:
                # Because we're replacing the initializer, we need to make sure
                # that any inherited initializers are also called.
                for init in [b.__init__._original for b in new_class.mro()
                             if issubclass(b, Component)
                             and '__init__' in b.__dict__]:
                    break
            def maybe_init(self, compmgr, init=init, cls=new_class):
                component_id = _component_id(cls)
                if component_id not in compmgr.components:
                    compmgr.components[component_id] = self
                    if init:
                        try:
                            init(self)
                        except:
                            del compmgr.components[component_id]
                            raise
            maybe_init._original = init
            new_class.__init__ = maybe_init

        if d.get('abstract'):
            # Don't put abstract component classes in the registry
            return new_class

        ComponentMeta._components.append(new_class)
        
        # if there are interfaces implemented by this class, 
        # a class adivsor calling _register_interfaces
        # will be called when zope.interface has finished 
        # working on it. Otherwise, we just register now
        # to pick up any inherited interfaces. 
        if new_class.__dict__.get('__implements_advice_data__'):
            return new_class
        else:
            return _register_interfaces(new_class)
            
def _register_interfaces(cls):
    # skip classes that were not determined to be 
    # concrete Components by the component metaclass.
    
    if not cls in ComponentMeta._components:
        return cls
        
    registry = ComponentMeta._registry
    for interface in zi.implementedBy(cls).__iro__:
        if interface.extends(ExtensionInterface):
            registry.setdefault(interface, [])
            if not cls in registry[interface]:
                registry[interface].append(cls)
                
    return cls

##############################################################################
# XXX monkey patch for mixing with zope.interface
# this monkey patch allows us to attach an additional class advisor that
# is executed after the class advisor generated by any of the implements()
# type declarations. The class advisor allows us to register the interfaces
# that are set up by the zope.interface class advisor.
import sys
from zope.interface import declarations
from zope.interface.declarations import _implements_advice
def _patched_implements(name, interfaces, classImplements):
    frame = sys._getframe(2)
    locals = frame.f_locals

    # Try to make sure we were called from a class def. In 2.2.0 we can't
    # check for __module__ since it doesn't seem to be added to the locals
    # until later on.
    if (locals is frame.f_globals) or (
        ('__module__' not in locals) and sys.version_info[:3] > (2, 2, 0)):
        raise TypeError(name+" can be used only from a class definition.")

    if '__implements_advice_data__' in locals:
        raise TypeError(name+" can be used only once in a class definition.")

    locals['__implements_advice_data__'] = interfaces, classImplements
    addClassAdvisor(_implements_advice, depth=3)
    addClassAdvisor(_register_interfaces, depth=3)
declarations._implements = _patched_implements
###############################################################################

def implements(*interfaces):
    """
    Declare a list of ExtensionInterfaces implemented by a 
    Component.
    """
    _patched_implements("implements", interfaces, zi.classImplements)
    

def implements_only(*interfaces):
    """
    declare that a Component implements exactly the list 
    of ExtensionInterfaces specified, overriding any 
    inherited declarations of implemented ExtensionInterfaces.
    """
    _patched_implements("implementsOnly", interfaces, zi.classImplementsOnly)

def implemented_by(thang):
    """
    return the list of ExtensionInterfaces implemented by a Component
    or Component type.
    """
    if isinstance(thang, type):
        get_ifaces = zi.implementedBy
    else: 
        get_ifaces = zi.providedBy

    ifaces = []
    for cls in get_ifaces(thang).__iro__:
        if hasattr(cls, 'extends') and cls.extends(ExtensionInterface):
            ifaces.append(cls)
    return ifaces
    
def is_implemented_by(cls, iface):
    """
    returns True if cls implements the interface given
    """
    return iface in implemented_by(cls)
    
def _component_id(component):
    if isinstance(component, basestring):
        return component

    if not isinstance(component, type):
        component = component.__class__

    return "%s.%s" % (component.__module__, component.__name__)

class Component(object):
    """Base class for components.

    Every component can declare what extension points it provides, as well as
    what extension points of other components it extends.
    """
    __metaclass__ = ComponentMeta

    def __new__(cls, *args, **kwargs):
        """Return an existing instance of the component if it has already been
        activated, otherwise create a new instance.
        """
        # If this component is also the component manager, just invoke that
        if issubclass(cls, ComponentManager):
            self = super(Component, cls).__new__(cls)
            self.compmgr = self
            return self

        # The normal case where the component is not also the component manager
        compmgr = args[0]
        component_id = _component_id(cls)
        self = compmgr.components.get(component_id)
        if self is None:
            self = super(Component, cls).__new__(cls)
            self.compmgr = compmgr
            compmgr.component_activated(self)
        return self


class ComponentManager(object):
    """The component manager keeps a pool of active components."""

    def __init__(self):
        """Initialize the component manager."""
        self.components = {}
        if isinstance(self, Component):
            my_id = _component_id(self)
            self.components[my_id] = self
        self._restriction = None

    def __contains__(self, cls):
        """Return wether the given class is in the list of active components."""
        return _component_id(cls) in self.components

    def __getitem__(self, cls):
        """Activate the component instance for the given class, or return the
        existing the instance if the component has already been activated.
        """
        if not self.is_component_enabled(cls):
            return None

        component_id = _component_id(cls)
        component = self.components.get(component_id)
        if component is None:
            if cls not in ComponentMeta._components:
                raise ExtensionError('Component "%s" not registered' % cls.__name__)
            try:
                component = cls(self)
            except TypeError, e:
                raise ExtensionError('Unable to instantiate component %r (%s)' %
                                (cls, e))
        return component

    def component_activated(self, component):
        """Can be overridden by sub-classes so that special initialization for
        components can be provided.
        """
    
    def restrict(self, policy):
        """
        restrict enabled components according to the policy 
        given -- is_component_enabled will be delegated to the 
        object specified.
        """
        self._restriction = policy

    def is_component_enabled(self, cls):
        """Controlled by policy given at construction time, but can be overridden 
        by sub-classes.

        If this method returns False, the component with the given class will
        not be available.
        
        By default, this method returns True
        """
        if self._restriction is None:
            return True
        else:
            return self._restriction.is_component_enabled(cls)