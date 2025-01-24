from pathlib import Path
from typing import Optional

from geotoolkit.utils.config import ConfigManager
from geotoolkit.utils import setup_logger
from geotoolkit.core import EngineType

# Package metadata
__version__ = "0.1.0"
__author__ = "Ray Thurman"
__email__ = "raymondthurman5@gmail.com"

# Initialize configuration
config_manager = ConfigManager()

# Set up package-level logger
logger = setup_logger(
    name="geotoolkit",
    log_level=config_manager.config.log_level,
    log_dir=config_manager.config.log_dir
)


def initialize(
        preferred_engine: str = EngineType.AUTO.value,
        log_level: str = "INFO",
        log_dir: Optional[Path] = None,
        workspace: Optional[Path] = None,
        config_file: Optional[Path] = None
) -> None:
    """
    Initialize GeoToolKit with custom configuration.

    Args:
        preferred_engine: Preferred GIS engine ('arcpy', 'gdal', or 'auto')
        log_level: Logging level
        log_dir: Directory for log files
        workspace: Default workspace directory
        config_file: Path to configuration file

    Raises:
        ConfigurationError: If configuration is invalid
    """
    global logger

    # Load config file if provided
    if config_file:
        config_manager.load_config(config_file)

    # Update configuration
    config_manager.update_config(
        preferred_engine=preferred_engine,
        log_level=log_level,
        log_dir=log_dir,
        workspace=workspace
    )

    # Reinitialize logger with new configuration
    logger = setup_logger(
        name="geotoolkit",
        log_level=config_manager.config.log_level,
        log_dir=config_manager.config.log_dir
    )

    logger.info(f"GeoToolKit initialized with engine: {preferred_engine}")
