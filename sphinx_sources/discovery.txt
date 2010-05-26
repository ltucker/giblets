=====================
Plugin Discovery
=====================

After any Component's module is imported, it will be registered and available to all ComponentManagers unless disabled.  Giblets provides a few methods for hinting at what modules need to be imported to discover the plugins in the current environment.

By Path
========

giblets.search.find_plugins_in_path(search_path)

imports each py file found in the search path given, which may be a path or a list 
of paths.

By Entry Point
===============

giblets.search.find_plugins_by_entry_point(entry_point_id)

imports modules listed in the given distutils entrypoint, typically listed in a package's setup.py.

For example, the ``sweetphoto`` app might use the entrypoint ``sweetphoto_plugins``.  

if Fancy inc. wanted to ship a plugin package called ``fancy_tools``, they might include a ``entry_points`` section like this in the fancy_tools setup.py to insure that the modules ``fancy_tools.brush`` and ``fancy_tools.eraser`` were imported.

    | entry_points = """
    | [sweetphoto_plugins]
    | fancy_brush = fancy_tools.brush
    | fancy_eraser = fancy_tools.eraser
    | """


    
