import json
from pathlib import Path


def get_epsg_code(target_region):
    if isinstance(target_region, int):
        return target_region

    if not isinstance(target_region, str):
        raise TypeError("Target region must be a string or integer.")

    regions_path = Path('regions.json')
    try:
        with regions_path.open('r') as f:
            regions_config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Regions file not found at {regions_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in regions file: {regions_path}")

    region_info = regions_config.get(target_region.upper())
    if region_info is None:
        raise ValueError(f"Target region '{target_region}' not found in regions file.")

    if 'epsg' not in region_info:
        raise ValueError(f"EPSG code not found for region '{target_region}'")

    return region_info['epsg']