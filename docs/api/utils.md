# Utils API Reference

The utils module provides utility functions and classes for configuration, logging, and other common operations.

## Configuration

### ConfigManager

::: geotoolkit.utils.config.ConfigManager
    options:
        show_root_heading: true
        show_source: true
        members: true

### GeoToolKitConfig

::: geotoolkit.utils.config.GeoToolKitConfig
    options:
        show_root_heading: true
        show_source: true
        members: true

## Logging

### setup_logger

::: geotoolkit.utils.logger.setup_logger
    options:
        show_root_heading: true
        show_source: true

### CustomFormatter

::: geotoolkit.utils.logger.CustomFormatter
    options:
        show_root_heading: true
        show_source: true
        members: true

### JSONFormatter

::: geotoolkit.utils.logger.JSONFormatter
    options:
        show_root_heading: true
        show_source: true
        members: true

## EPSG Utilities

### get_epsg_code

::: geotoolkit.utils.read_epsg.get_epsg_code
    options:
        show_root_heading: true
        show_source: true

## Common Usage Patterns

### Configuration Management

```python
from geotoolkit.utils.config import ConfigManager

# Get config instance
config = ConfigManager()

# Update configuration
config.update_config(
    preferred_engine='gdal',
    max_threads=8
)

# Save configuration
config.save_config('config.json')
```

### Logging Setup

```python
from geotoolkit.utils.logger import setup_logger
from pathlib import Path

# Set up logger
logger = setup_logger(
    name='geotoolkit',
    log_level='DEBUG',
    log_dir=Path('logs')
)

# Use logger
logger.info('Processing started')
logger.debug('Detailed information')
logger.error('Error occurred')
```

### EPSG Code Lookup

```python
from geotoolkit.utils.read_epsg import get_epsg_code

# Get EPSG code for a region
epsg = get_epsg_code('NAD83')
```

## Best Practices

1. **Configuration**
   - Use a single ConfigManager instance
   - Save configuration changes to file
   - Validate configuration values

2. **Logging**
   - Set appropriate log levels
   - Use structured logging
   - Rotate log files regularly

3. **Error Handling**
   - Handle configuration errors gracefully
   - Provide meaningful error messages
   - Log errors with context
