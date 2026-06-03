# -*- coding: utf-8 -*-

import sys
import os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))

# IMPORTANT: The import-order is crucial. 'lib' must be inserted last to stay at sys.path[0].
#  This prevents local modules or global packages from shadowing it.
sys.path.insert(0, os.path.join(parent_folder_path, 'plugin'))
sys.path.insert(0, parent_folder_path)
sys.path.insert(0, os.path.join(parent_folder_path, 'lib'))

from plugin.query import Query
from pyflowlauncher import Plugin

if __name__ == "__main__":
    plugin = Plugin()
    plugin.add_method(Query(plugin))
    plugin.run()
