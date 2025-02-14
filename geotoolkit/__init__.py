from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from .engines.gdal_engine.preprocessor import GDALPreprocessor
from .utils.config import ConfigManager
from .utils.logger import setup_logger

global logger


class Preprocessor:
    """High-level interface for preprocessing operations"""

    def __init__(self, engine: Optional[str] = None):
        self.engine = engine or ConfigManager().config.preferred_engine
        self._preprocessor = PreprocessorFactory.create(self.engine)

    def __getattr__(self, name):
        """Delegate methods to engine implementation"""
        return getattr(self._preprocessor, name)


class PreprocessorFactory:
    """Factory for creating preprocessor instances"""

    @staticmethod
    def create(engine: str):
        if engine.lower() == "gdal":
            return GDALPreprocessor()
        elif engine == "arcpy":
            from .engines.arcpy_engine.preprocessor import ArcPyPreprocessor

            return ArcPyPreprocessor()
        else:
            raise ValueError(f"Unsupported engine: {engine}")


@contextmanager
def GeoToolKitContext(**kwargs):
    """Context manager for temporary settings"""
    config = ConfigManager()
    old_settings = config.config.__dict__.copy()

    try:
        config.update_config(**kwargs)
        yield
    finally:
        config.config.__dict__.update(old_settings)


def initialize(
    preferred_engine: str = "auto",
    log_level: str = "INFO",
    log_dir: Optional[Path] = None,
    workspace: Optional[Path] = None,
    config_file: Optional[Path] = None,
) -> None:
    """Initialize GeoToolKit with custom configuration"""
    config = ConfigManager()

    if config_file:
        config.load_config(config_file)

    config.update_config(
        preferred_engine=preferred_engine,
        log_level=log_level,
        log_dir=log_dir,
        workspace=workspace,
    )

    logger = setup_logger(
        name="geotoolkit",
        log_level=config.config.log_level,
        log_dir=config.config.log_dir,
    )

    logger.info(f"GeoToolKit initialized with engine: {preferred_engine}")
