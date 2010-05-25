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
from helpers import *

def test_implemented_by():
    clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint
    from giblets import ExtensionInterface, implements, implemented_by

    class IFoo(ExtensionInterface):
        pass
        
    class IBar(ExtensionInterface):
        pass
        
    class Foo(Component):
        implements(IFoo)
    
    class Bar(Component):
        implements(IBar)
        
    mgr = ComponentManager()
    foo = Foo(mgr)
    bar = Bar(mgr)
    
    assert IFoo in implemented_by(Foo)
    assert IFoo in implemented_by(foo)
    assert len(list(implemented_by(Foo))) == len(list(implemented_by(foo))) == 1
        
    assert IBar in implemented_by(Bar)
    assert IBar in implemented_by(bar)
    assert len(list(implemented_by(Bar))) == len(list(implemented_by(bar))) == 1        

def test_is_implemented_by():
    from giblets import Component, ComponentManager, ExtensionPoint
    from giblets import ExtensionInterface, implements, is_implemented_by

    class IFoo(ExtensionInterface):
        pass
        
    class IBar(ExtensionInterface):
        pass
        
    class Foo(Component):
        implements(IFoo)
    
    class Bar(Component):
        implements(IBar)
        
    mgr = ComponentManager()
    foo = Foo(mgr)
    bar = Bar(mgr)
    
    assert is_implemented_by(Foo, IFoo)
    assert is_implemented_by(foo, IFoo)
    assert not is_implemented_by(Foo, IBar)
    assert not is_implemented_by(foo, IBar)
    
    assert is_implemented_by(Bar, IBar)
    assert is_implemented_by(bar, IBar)
    assert not is_implemented_by(Bar, IFoo)
    assert not is_implemented_by(bar, IFoo)

def test_is_implemented_by_implements_only():
    
    from giblets import Component, ComponentManager, ExtensionPoint
    from giblets import ExtensionInterface, implements, is_implemented_by
    from giblets import implements_only

    class IVehicle(ExtensionInterface):
        pass

    class IFloat(ExtensionInterface):
        pass

    class IBoat(IVehicle):
        pass

    class Sailboat(Component):
        implements(IBoat, IFloat)

    mgr = ComponentManager()

    sailboat = Sailboat(mgr)
    assert is_implemented_by(Sailboat, IBoat)
    assert is_implemented_by(sailboat, IBoat)
    assert is_implemented_by(Sailboat, IFloat)
    assert is_implemented_by(sailboat, IFloat)
    assert is_implemented_by(Sailboat, IVehicle)
    assert is_implemented_by(sailboat, IVehicle)


    class Sloop(Sailboat):
       pass

    sloop = Sloop(mgr)
    assert is_implemented_by(Sloop, IBoat)
    assert is_implemented_by(sloop, IBoat)
    assert is_implemented_by(Sloop, IFloat)
    assert is_implemented_by(sloop, IFloat)
    assert is_implemented_by(Sloop, IVehicle)
    assert is_implemented_by(sloop, IVehicle)

    class BoatWithAHole(Sailboat):
        implements_only(IBoat)

    bwah = BoatWithAHole
    assert is_implemented_by(BoatWithAHole, IBoat)
    assert is_implemented_by(bwah, IBoat)
    assert not is_implemented_by(BoatWithAHole, IFloat)
    assert not is_implemented_by(bwah, IFloat)
    assert is_implemented_by(BoatWithAHole, IVehicle)
    assert is_implemented_by(bwah, IVehicle)


def test_extension_reg():
    clear_registry()
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
    assert id(train1) == id(Train(mgr1))
    
    # check that all of the extensions for the extension point were registered
    for cls in (EngineCar, PassengerCar, CafeCar, CabooseCar):
        assert has_exactly(1, cls, train1.cars)
    
    # check that the Zebra is not a part of the train
    assert has_exactly(0, Zebra, train1.cars)
    
    # create a different component manager and the train associated with it, 
    # check the same stuff...
    mgr2 = ComponentManager()
    train2 = Train(mgr2)
    assert id(train2) == id(Train(mgr2))
    for cls in (EngineCar, PassengerCar, CafeCar, CabooseCar):
        assert has_exactly(1, cls, train2.cars)
    assert has_exactly(0, Zebra, train2.cars)

    # now check that the trains and extensions produced by the
    # different component managers are different.
    assert train1 != train2
    for cls in (EngineCar, PassengerCar, CafeCar, CabooseCar):
        i1 = (x for x in train1.cars if isinstance(x, cls)).next()
        i2 = (x for x in train2.cars if isinstance(x, cls)).next()
        assert id(i1) != id(i2)
        
        
def test_multi_extension():
    clear_registry()
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
        therefore wheeled and flying because the 
        interface inherits from both.
        """
        implements(IFlyingCar)


    class WheeledBalloon(Component):
        """
        This class is wheeled and flying, but is 
        not a flying car. 
        """
        implements(IWheeledVehicle, IFlyingVehicle)

    mgr = ComponentManager()
    
    # check that wheeled vehicles are in the parking lot
    parking_lot = ParkingLot(mgr)
    assert has_exactly(1, Sedan, parking_lot.vehicles)
    assert has_exactly(0, Helicopter, parking_lot.vehicles)
    assert has_exactly(1, FlyingBaloneyTruck, parking_lot.vehicles)
    assert has_exactly(1, WheeledBalloon, parking_lot.vehicles)
    
    # check that flying vehicles are in the airport
    airport = Airport(mgr)
    assert has_exactly(0, Sedan, airport.vehicles)
    assert has_exactly(1, Helicopter, airport.vehicles)
    assert has_exactly(1, FlyingBaloneyTruck, airport.vehicles)
    assert has_exactly(1, WheeledBalloon, airport.vehicles)
    
    # check that flying cars are in the flying parking lot
    flying_lot = FlyingParkingLot(mgr)
    assert has_exactly(0, Sedan, flying_lot.vehicles)
    assert has_exactly(0, Helicopter, flying_lot.vehicles)
    assert has_exactly(1, FlyingBaloneyTruck, flying_lot.vehicles)
    assert has_exactly(0, WheeledBalloon, flying_lot.vehicles)
    
    

def test_custom_mgr():
    clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements

    class ICog(ExtensionInterface):
        pass

    class Widget(Component):
        cogs = ExtensionPoint(ICog)

    class GoodCog(Component):
        implements(ICog)

    class BadCog(Component):
        implements(ICog)
    
    # custom component manager
    class FilterComponentManager(ComponentManager):
        def is_component_enabled(self, cls):
            return cls != BadCog
    
    mgr = FilterComponentManager()
    widget = Widget(mgr)
    assert has_exactly(1, GoodCog, widget.cogs)
    assert has_exactly(0, BadCog, widget.cogs)

def test_inherited_interfaces():
    clear_registry()
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
    assert has_exactly(3, Thing1, sorter.thing1)
    assert has_exactly(2, Thing3, sorter.thing1)
    assert has_exactly(1, Thing4, sorter.thing1)
    
    assert len(sorter.thing2) == 3
    assert has_exactly(3, Thing2, sorter.thing2)
    assert has_exactly(2, Thing3, sorter.thing2)
    assert has_exactly(1, Thing4, sorter.thing2)
    
    assert len(sorter.thing3) == 2
    assert has_exactly(2, Thing3, sorter.thing3)
    assert has_exactly(1, Thing4, sorter.thing3)
    
    assert len(sorter.thing4) == 1
    assert has_exactly(1, Thing4, sorter.thing4)
    
    
    
def test_abstract_component():
    clear_registry()
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
    assert has_exactly(1, ConcreteThing, thingbox.things)
    
def test_implements_only():
    clear_registry()
    from giblets import Component, ComponentManager, ExtensionPoint, ExtensionInterface, implements, implements_only

    class ICog(ExtensionInterface):
        pass
        
    class IWidget(ExtensionInterface):
        pass
        
    class Cog(Component):
        implements(ICog)
        
    class CogWidget(Cog):
        implements(IWidget)
        
    class NoCogWidget(Cog):
        implements_only(IWidget)
        
    class Machine(Component):
        cogs = ExtensionPoint(ICog)
        widgets = ExtensionPoint(IWidget)
        
    mgr = ComponentManager()
    machine = Machine(mgr)
    
    assert len(machine.cogs) == 2
    assert has_exactly(2, Cog, machine.cogs)
    assert has_exactly(1, CogWidget, machine.cogs)
    assert has_exactly(0, NoCogWidget, machine.cogs)
    
    assert len(machine.widgets) == 2
    assert has_exactly(1, CogWidget, machine.widgets)
    assert has_exactly(1, NoCogWidget, machine.widgets)
