Giblets
===================================

Giblets is a simple plugin system based on the component architecture 
of `Trac <http://trac.edgewall.org/>`_.  In a nutshell, giblets allows you to declare interfaces and discover components that implement them without coupling.  

Giblets also includes plugin discovery based on file paths or entry points along with flexible means to manage which components are enabled or disabled in your application.

Source Code
===========

Visit http://github.com/ltucker/giblets for current source and releases.

To grab the latest source right away::

    $ git clone http://github.com/ltucker/giblets.git

Installation 
============

You can install ``giblets`` from the Python Package Index (PyPI) using ``pip`` or ``easy_install``::

    $ pip install giblets
    
If you downloaded a source tarball::

    $ tar -xzf giblets-x.y.tgz
    $ cd giblets
    $ python setup.py install

You can also install the current development version of giblets with::

    $ pip install giblets==dev



Documentation 
=====================

.. toctree::
   :maxdepth: 2

   introduction
   components
   interfaces
   management
   discovery
  
* :ref:`genindex`
* :ref:`modindex`

