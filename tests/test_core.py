# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Luke Tucker
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: Luke Tucker <ltucker@openplans.org>
#


def test_extension_reg():
    _clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements


    # a Train is extended by a bunch of train cars...
    class ITrainCar(ExtensionInterface):
        pass

    class Train(Component):
        cars = ExtensionPoint(ITrainCar)

    class EngineCar(Component):
        implements(ITrainCar)
        
    class PassengerCar(Component):
        implements(ITrainCar)
        
    class CafeCar(Component):
        implements(ITrainCar)
    
    class CabooseCar(Component):
        implements(ITrainCar)
        

    # an irrelevant interface and implementation...
    class IZooAnimal(ExtensionInterface):
        pass
        
    class Zebra(Component):
        implements(IZooAnimal)

    # create a component manager and the train associated with it 
    mgr1 = ComponentManager()
    train1 = Train(mgr1)
    
    # components are singletons w/ respect to manager
    assert train1 == Train(mgr1)
    
    # check that all of the extensions for the extension point were registered
    for cls in [EngineCar, PassengerCar, CafeCar, CabooseCar]:
        assert _has_exactly(1, cls, train1.cars)
    
    # check that the Zebra is not a part of the train
    assert _has_exactly(0, Zebra, train1.cars)
    
    # create a different component manager and the train associated with it, 
    # check the same stuff...
    mgr2 = ComponentManager()
    train2 = Train(mgr2)
    assert train2 == Train(mgr2)
    for cls in [EngineCar, PassengerCar, CafeCar, CabooseCar]:
        assert _has_exactly(1, cls, train2.cars)
    assert _has_exactly(0, Zebra, train2.cars)

    # now check that the trains and extensions produced by the
    # different component managers are different.
    assert train1 != train2
    for cls in [EngineCar, PassengerCar, CafeCar, CabooseCar]:
        i1 = filter(lambda x: isinstance(x, cls), train1.cars)[0]
        i2 = filter(lambda x: isinstance(x, cls), train2.cars)[0]
        assert i1 != i2
        
        
def test_multi_extension():
    _clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements
    
    # set up some scenarios that test components providing multiple 
    # extensions and extension interfaces that imply other 
    # extension interfaces by inheritance
        
    # a parking lot gets all wheeled vehicles
    class IWheeledVehicle(ExtensionInterface):
        pass
    class ParkingLot(Component):
        vehicles = ExtensionPoint(IWheeledVehicle)

    # an airport gets all flying vehicles
    class IFlyingVehicle(ExtensionInterface):
        pass
    class Airport(Component):
        vehicles = ExtensionPoint(IFlyingVehicle)
    
    # a flying parking lot is only populated by flying cars, 
    # which also happen to be wheeled and flying
    class IFlyingCar(IWheeledVehicle, IFlyingVehicle):
        pass
    class FlyingParkingLot(Component):
        vehicles = ExtensionPoint(IFlyingCar)

    # now some vehicles implementing the various types...    
    class Sedan(Component):
        """
        This class is only a wheeled vehicle
        """
        implements(IWheeledVehicle)

    class Helicopter(Component):
        """
        This class is only a flying vehicle
        """
        implements(IFlyingVehicle)
        
    class FlyingBaloneyTruck(Component):
        """
        This class is a flying car, it is also 
        therefor wheeled and flying because the 
        interface inherits from both.
        """
        implements(IFlyingCar)


    class WheeledBalloon(Component):
        """
        This class is wheeled and flys, but is 
        not a flying car. 
        """
        implements(IWheeledVehicle, IFlyingVehicle)

    mgr = ComponentManager()
    
    # check that wheeled vehicles are in the parking lot
    parking_lot = ParkingLot(mgr)
    assert _has_exactly(1, Sedan, parking_lot.vehicles)
    assert _has_exactly(0, Helicopter, parking_lot.vehicles)
    assert _has_exactly(1, FlyingBaloneyTruck, parking_lot.vehicles)
    assert _has_exactly(1, WheeledBalloon, parking_lot.vehicles)
    
    # check that flying vehicles are in the airport
    airport = Airport(mgr)
    assert _has_exactly(0, Sedan, airport.vehicles)
    assert _has_exactly(1, Helicopter, airport.vehicles)
    assert _has_exactly(1, FlyingBaloneyTruck, airport.vehicles)
    assert _has_exactly(1, WheeledBalloon, airport.vehicles)
    
    # check that flying cars are in the flying parking lot
    flying_lot = FlyingParkingLot(mgr)
    assert _has_exactly(0, Sedan, flying_lot.vehicles)
    assert _has_exactly(0, Helicopter, flying_lot.vehicles)
    assert _has_exactly(1, FlyingBaloneyTruck, flying_lot.vehicles)
    assert _has_exactly(0, WheeledBalloon, flying_lot.vehicles)
    
def test_blacklist_mgr():
    _clear_registry()
    from giblets import Component, BlacklistComponentManager, ExtensionPoint, ExtensionInterface, implements
    
    class ICog(ExtensionInterface):
        pass
        
    class Widget(Component):
        cogs = ExtensionPoint(ExtensionInterface)
     
    class GoodCog(Component):
        implements(ICog)
        
    class BadCog(Component):
        implements(ICog)
        
    # first no restrtictions, both should show up
    mgr = BlacklistComponentManager()
    widget = Widget(mgr)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(1, BadCog, widget.cogs)
    
    # try force-disabling in this mgr
    mgr.disable_component(BadCog)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    # re-enable
    mgr.enable_component(BadCog)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(1, BadCog, widget.cogs)

    mgr.disable_component('tests.test_core.BadCog')
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    mgr.enable_component('tests.test_core.BadCog')
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(1, BadCog, widget.cogs)


def test_whitelist_mgr():
    _clear_registry()
    from giblets import Component, WhitelistComponentManager, ExtensionPoint, ExtensionInterface, implements

    class ICog(ExtensionInterface):
        pass

    class Widget(Component):
        cogs = ExtensionPoint(ExtensionInterface)

    class GoodCog(Component):
        implements(ICog)

    class BadCog(Component):
        implements(ICog)

    # first nothing specified, nothing should show up
    mgr = WhitelistComponentManager()
    widget = Widget(mgr)
    assert _has_exactly(0, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    # enable only the GoodCog
    mgr.enable_component(GoodCog)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    # re-disable, should show nothing again
    mgr.disable_component(GoodCog)
    assert _has_exactly(0, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    # try enable by name...
    mgr.enable_component('tests.test_core.GoodCog')
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    mgr.disable_component('tests.test_core.GoodCog')
    assert _has_exactly(0, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)


def test_pattern_manager():
    _clear_registry()
    from giblets import Component, PatternComponentManager, ExtensionPoint, ExtensionInterface, implements
    
    class ICog(ExtensionInterface):
        pass

    class Widget(Component):
        cogs = ExtensionPoint(ExtensionInterface)

    class GoodCog(Component):
        implements(ICog)

    class BadCog(Component):
        implements(ICog)

    mgr = PatternComponentManager()
    widget = Widget(mgr)

    # to start with, everything is disabled...
    assert _has_exactly(0, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

    # easy to enable everything...
    mgr.append_pattern('*', enable=True)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(1, BadCog, widget.cogs)

    # now just disable the bad one
    mgr.append_pattern('tests.test_core.BadCog', enable=False)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)
    
    # disable all the test core components...
    mgr.append_pattern('tests.test_core.*', enable=False)    
    assert _has_exactly(0, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)
    

def test_custom_mgr():
    _clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements

    class ICog(ExtensionInterface):
        pass

    class Widget(Component):
        cogs = ExtensionPoint(ExtensionInterface)

    class GoodCog(Component):
        implements(ICog)

    class BadCog(Component):
        implements(ICog)
    
    # custom component manager
    class FilterComponentManager(ComponentManager):
        def is_component_enabled(self, cls):
            if cls == BadCog:
                return False
            else:
                return True
    
    mgr = FilterComponentManager()
    widget = Widget(mgr)
    assert _has_exactly(1, GoodCog, widget.cogs)
    assert _has_exactly(0, BadCog, widget.cogs)

def test_inherited_interfaces():
    _clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements

    class IThing1(ExtensionInterface):
        pass

    class IThing2(ExtensionInterface):
        pass

    class IThing3(ExtensionInterface):
        pass

    class IThing4(ExtensionInterface):
        pass
        
    class Thing1(Component):
        implements(IThing1)
    
    class Thing2(Component):
        implements(IThing2)
    
    class Thing3(Thing1, Thing2):
        implements(IThing3)
        
    class Thing4(Thing3):
        implements(IThing4)
        
    class ThingSorter(Component):
        thing1 = ExtensionPoint(IThing1)
        thing2 = ExtensionPoint(IThing2)
        thing3 = ExtensionPoint(IThing3)
        thing4 = ExtensionPoint(IThing4)
        
    mgr = ComponentManager()
    sorter = ThingSorter(mgr)
    
    assert len(sorter.thing1) == 3
    assert _has_exactly(3, Thing1, sorter.thing1)
    assert _has_exactly(2, Thing3, sorter.thing1)
    assert _has_exactly(1, Thing4, sorter.thing1)
    
    assert len(sorter.thing2) == 3
    assert _has_exactly(3, Thing2, sorter.thing2)
    assert _has_exactly(2, Thing3, sorter.thing2)
    assert _has_exactly(1, Thing4, sorter.thing2)
    
    assert len(sorter.thing3) == 2
    assert _has_exactly(2, Thing3, sorter.thing3)
    assert _has_exactly(1, Thing4, sorter.thing3)
    
    assert len(sorter.thing4) == 1
    assert _has_exactly(1, Thing4, sorter.thing4)
    
    
    
def test_abstract_component():
    _clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements
    
    class ISomething(ExtensionInterface):
        pass

    class BaseThing(Component):
        implements(ISomething)
        abstract = True

    class ConcreteThing(BaseThing):
        pass

    class ThingBox(Component):
        things = ExtensionPoint(ISomething)

    mgr = ComponentManager()
    
    thingbox = ThingBox(mgr)

    assert len(thingbox.things) == 1
    assert _has_exactly(1, ConcreteThing, thingbox.things)
    
def test_implementsOnly():
    _clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements, implementsOnly

    class ICog(ExtensionInterface):
        pass
        
    class IWidget(ExtensionInterface):
        pass
        
    class Cog(Component):
        implements(ICog)
        
    class CogWidget(Cog):
        implements(IWidget)
        
    class NoCogWidget(Cog):
        implementsOnly(IWidget)
        
    class Machine(Component):
        cogs = ExtensionPoint(ICog)
        widgets = ExtensionPoint(IWidget)
        
    mgr = ComponentManager()
    machine = Machine(mgr)
    
    assert len(machine.cogs) == 2
    assert _has_exactly(2, Cog, machine.cogs)
    assert _has_exactly(1, CogWidget, machine.cogs)
    assert _has_exactly(0, NoCogWidget, machine.cogs)
    
    assert len(machine.widgets) == 2
    assert _has_exactly(1, CogWidget, machine.widgets)
    assert _has_exactly(1, NoCogWidget, machine.widgets)
    
    
def _has_exactly(k, T, l):
    """
    test that the list L has exactly k members that are 
    instances of the type T
    """
    return len(filter(lambda x: isinstance(x, T), l)) == k

def _clear_registry():
    from giblets.core import ComponentMeta
    ComponentMeta._registry = {}
    ComponentMeta._components = []
