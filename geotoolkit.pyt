import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("geotoolkit")))

from geotoolkit.toolboxes.sinuosity_toolbox import CalculateSinuosity


class GeoToolkit(object):
    def __init__(self):
        self.label = "GeoToolkit Toolbox"
        self.alias = "geotoolkit"
        self.tools = [CalculateSinuosity]
