import os
import sys

sys.path.append(os.path.dirname(__file__)).joinpath("geotoolkit")

from geotoolkit.toolboxes import CalculateSinuosity


class GeoToolkit(object):
    def __init__(self):
        self.label = "GeoToolkit Toolbox"
        self.alias = "geotoolkit"
        self.tools = [CalculateSinuosity]
