# -*- coding: utf-8 -*-

import sys
import os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from plugin.query import Query
from pyflowlauncher import Plugin

if __name__ == "__main__":
    plugin = Plugin()
    plugin.add_method(Query(plugin))
    plugin.run()
