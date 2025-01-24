from enum import Enum
from typing import Dict, List


class EngineType(Enum):
    """Supported GIS engines"""
    ARCPY = "arcpy"
    GDAL = "gdal"
    AUTO = "auto"


class ProcessingMode(Enum):
    """Processing modes for operations"""
    BASIC = "basic"
    ADVANCED = "advanced"
    BATCH = "batch"


class GeometryType(Enum):
    """Supported geometry types"""
    POINT = "point"
    LINE = "line"
    POLYGON = "polygon"
    MULTIPOINT = "multipoint"
    MULTILINE = "multiline"
    MULTIPOLYGON = "multipolygon"


# Common coordinate systems
COMMON_PROJECTIONS: Dict[str, int] = {
    "WGS84": 4326,
    "WEB_MERCATOR": 3857,
    "NAD83": 4269,
    "NAD83_UTM_ZONE_11N": 26911
}

# Default configuration
DEFAULT_CONFIG: Dict[str, any] = {
    "preferred_engine": EngineType.AUTO.value,
    "max_threads": 4,
    "log_level": "INFO",
    "chunk_size": 1000,
    "timeout": 300
}

# Supported file formats
SUPPORTED_VECTOR_FORMATS: List[str] = [
    "shp",
    "geojson",
    "gdb",
    "gpkg",
    "kml"
]

SUPPORTED_RASTER_FORMATS: List[str] = [
    "tif",
    "img",
    "jpg",
    "png",
    "dem"
]

# Processing constants
BUFFER_DISTANCES: Dict[str, float] = {
    "VERY_SMALL": 0.1,
    "SMALL": 1.0,
    "MEDIUM": 10.0,
    "LARGE": 100.0
}

# Validation thresholds
VALIDATION_THRESHOLDS: Dict[str, float] = {
    "MIN_AREA": 0.001,
    "MAX_VERTICES": 10000,
    "SNAP_TOLERANCE": 0.001,
    "CLUSTER_TOLERANCE": 0.001
}

# Error messages
ERROR_MESSAGES: Dict[str, str] = {
    "ENGINE_NOT_FOUND": "No supported GIS engine found. Install GDAL or ArcPy.",
    "INVALID_DATASET": "Dataset is invalid or corrupted: {dataset}",
    "PROJECTION_MISMATCH": "Projection mismatch between datasets",
    "LICENSE_REQUIRED": "Required license not available: {license}",
    "PROCESSING_FAILED": "Processing failed: {details}"
}
