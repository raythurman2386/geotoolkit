# Configuration Guide

GeoToolKit provides flexible configuration options through the `ConfigManager` class. This guide explains how to configure the library for your needs.

## Configuration Options

The following configuration options are available:

- `preferred_engine`: The preferred GIS engine to use ('arcpy', 'gdal', or 'auto')
- `max_threads`: Maximum number of threads for parallel processing
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_dir`: Directory for log files (optional)
- `workspace`: Default workspace directory (optional)
- `chunk_size`: Size of chunks for batch processing
- `timeout`: Operation timeout in seconds

## Using ConfigManager

### Basic Configuration

```python
from geotoolkit.utils.config import ConfigManager

# Get the config manager instance
config = ConfigManager()

# Update configuration
config.update_config(
    preferred_engine='gdal',
    max_threads=8,
    log_level='INFO',
    workspace='/path/to/workspace'
)
```

### Saving and Loading Configuration

You can save your configuration to a JSON file and load it later:

```python
from pathlib import Path

# Save configuration
config.save_config(Path('geotoolkit_config.json'))

# Load configuration
config.load_config(Path('geotoolkit_config.json'))
```

## Logging Configuration

GeoToolKit includes a robust logging system with both console and file output:

```python
from geotoolkit.utils.logger import setup_logger
from pathlib import Path

# Set up logger with custom configuration
logger = setup_logger(
    name='geotoolkit',
    log_level='DEBUG',
    log_dir=Path('/path/to/logs')
)
```

The logging system includes:
- Colored console output for different log levels
- JSON-formatted file output for machine parsing
- Automatic log rotation

## Engine Configuration

### Engine Selection

GeoToolKit supports multiple GIS engines:

```python
from geotoolkit import Preprocessor

# Auto-detect available engine
preprocessor = Preprocessor()

# Explicitly specify engine
preprocessor = Preprocessor(engine='gdal')
# or
preprocessor = Preprocessor(engine='arcpy')
```

### Engine-Specific Settings

Each engine may have its own specific settings that can be configured through the same configuration interface. Refer to the specific engine documentation for details.
