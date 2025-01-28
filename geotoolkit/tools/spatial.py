import json
from pathlib import Path
from typing import Dict, Union, Optional


class SpatialReference:
    """Utility class for handling spatial references."""

    def __init__(self):
        self.regions = self._load_regions()

    def _load_regions(self) -> Dict:
        """Load regions from JSON file."""
        regions_path = Path(__file__).parent.parent / "regions.json"
        try:
            with open(regions_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Regions file not found at {regions_path}")

    def get_proj4(self, region: str) -> str:
        """Get proj4 string for a region."""
        region = region.upper()
        if region not in self.regions:
            raise ValueError(f"Unknown region: {region}")
        return self.regions[region]["proj4"]

    def get_epsg(self, region: str) -> int:
        """Get EPSG code for a region."""
        region = region.upper()
        if region not in self.regions:
            raise ValueError(f"Unknown region: {region}")
        return self.regions[region]["epsg"]

    def get_region_info(self, region: str) -> Dict:
        """Get all information for a region."""
        region = region.upper()
        if region not in self.regions:
            raise ValueError(f"Unknown region: {region}")
        return self.regions[region]
