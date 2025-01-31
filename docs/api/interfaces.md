# Interfaces API Reference

The interfaces module provides the main user-facing classes for GeoToolKit functionality.

## Preprocessor

::: geotoolkit.interfaces.preprocessor.Preprocessor
    options:
        show_root_heading: true
        show_source: true
        members: true

## Common Usage Patterns

### Basic Initialization

```python
from geotoolkit import Preprocessor

# Auto-detect engine
preprocessor = Preprocessor()
```

### Explicit Engine Selection

```python
# Use GDAL engine
preprocessor = Preprocessor(engine='gdal')

# Use ArcPy engine
preprocessor = Preprocessor(engine='arcpy')
```

### Data Processing

```python
# Clean field names
preprocessor.clean_field_names('input_data.shp')

# Standardize projection
preprocessor.standardize_projection(
    'input_data.shp',
    'EPSG:4326'
)
```

## Interface Design

The interfaces module follows these design principles:

1. **Unified Interface**: Consistent API regardless of the underlying engine
2. **Engine Abstraction**: Engine-specific details are hidden from the user
3. **Error Handling**: Comprehensive error handling and reporting
4. **Type Safety**: Strong typing and input validation
5. **Documentation**: Detailed docstrings and type hints

## Best Practices

When using the interfaces:

1. **Engine Selection**
   - Use auto-detection unless specific engine features are needed
   - Verify engine availability before processing

2. **Error Handling**
   - Implement try-except blocks for robust error handling
   - Log errors appropriately
   - Provide user feedback

3. **Resource Management**
   - Close resources when done
   - Use context managers where applicable
   - Monitor memory usage

4. **Performance**
   - Process large datasets in chunks
   - Use appropriate batch sizes
   - Consider parallel processing options
