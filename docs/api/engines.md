# Engines API Reference

GeoToolKit supports multiple GIS engines through specialized implementations. This section documents the available engine implementations.

## GDAL Engine

### GDALPreprocessor

::: geotoolkit.engines.gdal_engine.preprocessor.GDALPreprocessor
    options:
        show_root_heading: true
        show_source: true
        members: true

## ArcPy Engine

### ArcPyPreprocessor

::: geotoolkit.engines.arcpy_engine.preprocessor.ArcPyPreprocessor
    options:
        show_root_heading: true
        show_source: true
        members: true

## Engine Selection

The appropriate engine is selected based on:

1. Explicit user choice through the `engine` parameter
2. Available system dependencies
3. Configuration settings

### Auto-Detection Logic

When `engine='auto'` is specified (default):

1. First attempts to load ArcPy engine if ArcGIS Pro is installed
2. Falls back to GDAL engine if ArcPy is not available
3. Raises `EngineNotFoundError` if no supported engine is found

### Engine Capabilities

Each engine implementation provides:

- Standard interface defined by base classes
- Engine-specific optimizations
- Custom error handling
- Performance monitoring

## Engine-Specific Features

### GDAL Features

- Open-source implementation
- Cross-platform support
- Wide format support
- Memory-efficient processing
- Direct file access

### ArcPy Features

- ArcGIS Pro integration
- Enterprise geodatabase support
- Advanced geoprocessing
- ArcGIS workspace management
- License-based functionality
