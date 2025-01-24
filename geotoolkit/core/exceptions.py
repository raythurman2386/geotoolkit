class GeoToolKitError(Exception):
    """Base exception class for GeoToolKit"""
    pass


class EngineNotFoundError(GeoToolKitError):
    """Raised when no supported GIS engine is found"""
    pass


class EngineInitializationError(GeoToolKitError):
    """Raised when engine initialization fails"""
    pass


class DatasetNotFoundError(GeoToolKitError):
    """Raised when input dataset cannot be found"""
    pass


class InvalidDatasetError(GeoToolKitError):
    """Raised when dataset is invalid or corrupted"""
    pass


class ProjectionError(GeoToolKitError):
    """Raised when projection-related operations fail"""
    pass


class ValidationError(GeoToolKitError):
    """Raised when data validation fails"""
    pass


class ProcessingError(GeoToolKitError):
    """Raised when processing operations fail"""
    pass


class ConfigurationError(GeoToolKitError):
    """Raised when configuration is invalid"""
    pass


class LicenseError(GeoToolKitError):
    """Raised when required license is not available"""
    pass
