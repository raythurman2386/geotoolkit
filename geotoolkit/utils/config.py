# utils/config.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
import json
from ..core.constants import DEFAULT_CONFIG, EngineType
from ..core.exceptions import ConfigurationError


@dataclass
class GeoToolKitConfig:
    preferred_engine: str = DEFAULT_CONFIG["preferred_engine"]
    max_threads: int = DEFAULT_CONFIG["max_threads"]
    log_level: str = DEFAULT_CONFIG["log_level"]
    log_dir: Optional[Path] = None
    workspace: Optional[Path] = None
    chunk_size: int = DEFAULT_CONFIG["chunk_size"]
    timeout: int = DEFAULT_CONFIG["timeout"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            key: str(value) if isinstance(value, Path) else value
            for key, value in self.__dict__.items()
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "GeoToolKitConfig":
        """Create config from dictionary"""
        # Convert string paths to Path objects
        if "log_dir" in config_dict and config_dict["log_dir"]:
            config_dict["log_dir"] = Path(config_dict["log_dir"])
        if "workspace" in config_dict and config_dict["workspace"]:
            config_dict["workspace"] = Path(config_dict["workspace"])
        return cls(**config_dict)


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = GeoToolKitConfig()
        return cls._instance

    def update_config(self, **kwargs):
        """Update configuration with new values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                raise ConfigurationError(f"Invalid configuration key: {key}")

    def save_config(self, config_path: Path):
        """Save configuration to JSON file"""
        try:
            with open(config_path, "w") as f:
                json.dump(self.config.to_dict(), f, indent=4)
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")

    def load_config(self, config_path: Path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, "r") as f:
                config_dict = json.load(f)
            self.config = GeoToolKitConfig.from_dict(config_dict)
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")
