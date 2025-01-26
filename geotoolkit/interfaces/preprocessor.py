from ..core.exceptions import EngineNotFoundError
from ..engines.gdal_engine.preprocessor import GDALPreprocessor


class Preprocessor:
    def __init__(self, engine='auto'):
        self.engine = self._initialize_engine(engine)

    def _initialize_engine(self, engine):
        if engine == 'auto':
            try:
                from osgeo import gdal
                return GDALPreprocessor()
            except ImportError:
                raise EngineNotFoundError("No supported GIS engine found")
        elif engine == 'gdal':
            return GDALPreprocessor()
        else:
            raise ValueError(f"Unsupported engine: {engine}")

    def clean_field_names(self, dataset):
        return self.engine.clean_field_names(dataset)

    def standardize_projection(self, dataset, target_proj):
        return self.engine.standardize_projection(dataset, target_proj)