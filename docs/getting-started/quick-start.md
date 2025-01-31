# Quick Start Guide

This guide will help you get up and running with GeoToolKit quickly. We'll cover basic usage and common operations.

## Basic Usage

### Initialize Components

```python
from geotoolkit import Preprocessor, Analyzer, RasterTools

# Initialize with automatic engine detection
preprocessor = Preprocessor()
analyzer = Analyzer()
raster_tools = RasterTools()
```

### Specify Engine Preference

```python
# Initialize with specific engine
preprocessor = Preprocessor(engine='gdal')
# or
preprocessor = Preprocessor(engine='arcpy')
```

## Common Operations

### Data Preprocessing

```python
# Clean field names in a shapefile
preprocessor.clean_field_names("input_data.shp")

# Standardize data types
preprocessor.standardize_fields("input_data.shp")
```

### Spatial Analysis

```python
# Calculate basic statistics
results = analyzer.calculate_statistics("analysis_layer.shp")

# Perform spatial operations
buffer_result = analyzer.create_buffer("input.shp", "output.shp", distance=100)
```

### Raster Processing

```python
# Process raster data
raster_tools.resample("input.tif", "output.tif", cell_size=30)
```

## Configuration Management

You can configure GeoToolKit's behavior using the ConfigManager:

```python
from geotoolkit.utils.config import ConfigManager

# Configure default settings
config = ConfigManager()
config.update_config(
    preferred_engine='gdal',
    max_threads=8,
    workspace='/path/to/workspace'
)
```

## Next Steps

- Check out the [Configuration Guide](../user-guide/configuration.md) for detailed settings
- Learn more about [Preprocessor](../user-guide/preprocessor.md) capabilities
- Explore [Analyzer](../user-guide/analyzer.md) functionality
- Discover [RasterTools](../user-guide/raster-tools.md) features
