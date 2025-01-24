from osgeo import gdal, ogr
from ...core.base import BasePreprocessor


class GDALPreprocessor(BasePreprocessor):
    def clean_field_names(self, dataset):
        # GDAL-specific implementation
        pass

    def standardize_projection(self, dataset, target_proj):
        # GDAL-specific implementation
        pass