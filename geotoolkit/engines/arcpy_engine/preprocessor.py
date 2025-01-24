import arcpy
from pathlib import Path
from typing import Union, List, Optional, Dict
import re
from ...core.base import BasePreprocessor
from ...core.exceptions import ProcessingError
from ... import logger

class ArcPyPreprocessor(BasePreprocessor):
    """ArcPy implementation of preprocessing operations."""

    def clean_field_names(self, dataset: Union[str, Path],
                          exclude_fields: Optional[List[str]] = None) -> Union[str, Path]:
        """
        Clean field names using ArcPy.
        """
        try:
            # Create list of fields to process
            fields = arcpy.ListFields(str(dataset))
            field_mapping = {}

            for field in fields:
                if field.name in ['OBJECTID', 'SHAPE', 'FID', 'Shape']:
                    continue
                if exclude_fields and field.name in exclude_fields:
                    continue

                # Clean field name
                new_name = re.sub(r'[^a-zA-Z0-9_]', '_', field.name)
                new_name = re.sub(r'_+', '_', new_name)
                new_name = new_name.strip('_').lower()

                if new_name != field.name:
                    field_mapping[field.name] = new_name

            # Rename fields
            for old_name, new_name in field_mapping.items():
                arcpy.AlterField_management(
                    str(dataset),
                    old_name,
                    new_name
                )

            logger.info(f"Cleaned field names in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error cleaning field names: {str(e)}")

    def standardize_projection(self, dataset: Union[str, Path],
                               target_epsg: Union[int, str],
                               in_place: bool = False) -> Union[str, Path]:
        """
        Reproject dataset using ArcPy.
        """
        try:
            input_path = str(dataset)
            if not in_place:
                output_path = str(Path(input_path).with_suffix('')) + '_reprojected.shp'
            else:
                output_path = input_path

            # Create spatial reference object
            sr = arcpy.SpatialReference(target_epsg)

            # Project dataset
            arcpy.Project_management(
                input_path,
                output_path,
                sr
            )

            logger.info(f"Reprojected {dataset} to EPSG:{target_epsg}")
            return output_path

        except Exception as e:
            raise ProcessingError(f"Error reprojecting dataset: {str(e)}")

    def repair_geometry(self, dataset: Union[str, Path],
                        in_place: bool = False) -> Union[str, Path]:
        """
        Fix common geometry errors using ArcPy.
        """
        try:
            input_path = str(dataset)
            if not in_place:
                output_path = str(Path(input_path).with_suffix('')) + '_repaired.shp'
            else:
                output_path = input_path

            # Repair geometry
            arcpy.RepairGeometry_management(
                input_path,
                "DELETE_NULL"
            )

            logger.info(f"Repaired geometries in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error repairing geometries: {str(e)}")