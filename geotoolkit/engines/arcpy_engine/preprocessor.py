import arcpy
from ...core.base import BasePreprocessor


class ArcPyPreprocessor(BasePreprocessor):
    def clean_field_names(self, dataset):
        # ArcPy-specific implementation
        pass

    def standardize_projection(self, dataset, target_proj):
        # ArcPy-specific implementation
        pass