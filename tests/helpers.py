
 
def has_exactly(k, T, l):
    """
    test that the list l has exactly k members that are 
    instances of the type T
    """
    return sum(1 for x in l if isinstance(x, T)) == k

def clear_registry():
    from giblets.core import ComponentMeta
    ComponentMeta._registry = {}
    ComponentMeta._components = []
