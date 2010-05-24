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

from glob import glob
import imp
import os
import sys
import traceback

__all__ = ['find_plugins_in_path', 'find_plugins_by_entry_point']

import logging 
log = logging.getLogger(__name__)

def find_plugins_in_path(search_path):
    """
    Discover plugins in any .py files in the given on-disk locations eg:
    
    find_plugins_in_path("/path/to/mymodule/plugins")
    find_plugins_in_path(["/path/to/mymodule/plugins", "/some/more/plugins"])
    
    """
    if isinstance(search_path, basestring):
        search_path = [search_path]

    for path in search_path:
        log.debug("searching for plugins in %s" % search_path)
        for py_file in glob(os.path.join(path, '*.py')):
            try:
                module_name = os.path.basename(py_file[:-3])
                # if it's already loaded, move on 
                if module_name in sys.modules:
                    continue
                
                log.debug("Loading module %s" % py_file)
                module = imp.load_source(module_name, py_file)
            except:
                log.error("Error loading module %s: %s" % (os.path.join(path, py_file), traceback.format_exc()))



try:
    from pkg_resources import working_set as master_working_set

    def find_plugins_by_entry_point(entry_point_id, ws=master_working_set):
        for entry in ws.iter_entry_points(entry_point_id):
            log.debug('Loading plugin %s from %s', entry.name, entry.dist.location)

            try:
                entry.load(require=True)
            except:
                import traceback
                log.error("Error loading plugin %s from %s: %s" % (entry.name, entry.dist.location, traceback.format_exc()))
        
except ImportError:
    
    def find_plugins_by_entry_point(entry_point_id, ws=None):
        log.warning("Not loading plugins from eggs, setuptools not found.")