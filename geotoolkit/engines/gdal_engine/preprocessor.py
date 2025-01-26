import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Union, List, Optional
from osgeo import gdal, ogr, osr
import re

from ... import setup_logger
from ...core.base import BasePreprocessor
from ...core.exceptions import ProcessingError
from ...tools.spatial import SpatialReference
from ...utils.read_epsg import get_epsg_code

logger = setup_logger(
    "csv_processor",
    log_level="INFO",
    log_dir=Path(__file__).parent / 'logs',
)


class GDALPreprocessor(BasePreprocessor):
    """GDAL implementation of preprocessing operations."""

    def __init__(self):
        gdal.UseExceptions()  # Enable exception handling
        self.spatial_ref = SpatialReference()

    def clean_field_names(self, dataset: Union[str, Path],
                          exclude_fields: Optional[List[str]] = None) -> Union[str, Path]:
        """
        Clean field names using GDAL.
        
        Args:
            dataset: Path to input dataset
            exclude_fields: Fields to exclude from cleaning
            
        Returns:
            Path to processed dataset
        """
        try:
            ds = ogr.Open(str(dataset), 1)  # 1 for read-write
            if ds is None:
                raise ProcessingError(f"Could not open dataset: {dataset}")

            layer = ds.GetLayer()
            layer_defn = layer.GetLayerDefn()

            # Get field names and create mapping
            field_mapping = {}
            for i in range(layer_defn.GetFieldCount()):
                field = layer_defn.GetFieldDefn(i)
                old_name = field.GetName()

                if exclude_fields and old_name in exclude_fields:
                    continue

                # Clean field name: remove special chars, replace spaces
                new_name = re.sub(r'[^a-zA-Z0-9_]', '_', old_name)
                new_name = re.sub(r'_+', '_', new_name)  # Remove multiple underscores
                new_name = new_name.strip('_').lower()

                if new_name != old_name:
                    field_mapping[old_name] = new_name

            # Rename fields
            for old_name, new_name in field_mapping.items():
                layer.AlterFieldDefn(
                    layer_defn.GetFieldIndex(old_name),
                    ogr.FieldDefn(new_name, layer_defn.GetFieldDefn(
                        layer_defn.GetFieldIndex(old_name)).GetType()),
                    ogr.ALTER_NAME_FLAG
                )

            ds = None  # Close dataset
            logger.info(f"Cleaned field names in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error cleaning field names: {str(e)}")


    def standardize_projection(self, dataset: Union[str, Path], target_region: Union[str, int], in_place: bool = False) -> Union[str, Path]:
        try:
            epsg_code = get_epsg_code(target_region)

            input_path = Path(dataset)
            if in_place:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=input_path.suffix) as tmp:
                    temp_output = Path(tmp.name)
            else:
                # Create output file with '_reprojected' suffix
                temp_output = input_path.with_name(f"{input_path.stem}_reprojected{input_path.suffix}")

            # Set up ogr2ogr command
            cmd = [
                'ogr2ogr',
                '-f', 'ESRI Shapefile' if input_path.suffix.lower() == '.shp' else 'GeoJSON',
                '-s_srs', f'EPSG:{epsg_code}',
                '-t_srs', f'EPSG:{epsg_code}',
                str(temp_output),
                str(input_path)
            ]

            # Run ogr2ogr command
            subprocess.run(cmd, check=True)

            if in_place:
                # Replace the original file with the temporary file
                shutil.move(str(temp_output), str(input_path))
                return input_path
            else:
                return temp_output

        except Exception as e:
            raise RuntimeError(f"Error during reprojection: {str(e)}")

    def repair_geometry(self, dataset: Union[str, Path],
                        in_place: bool = False) -> Union[str, Path]:
        """
        Fix common geometry errors using GDAL.
        
        Args:
            dataset: Path to input dataset
            in_place: Whether to modify the input dataset or create new one
            
        Returns:
            Path to processed dataset
        """
        try:
            ds = ogr.Open(str(dataset), 1)
            if ds is None:
                raise ProcessingError(f"Could not open dataset: {dataset}")

            layer = ds.GetLayer()

            for feature in layer:
                geom = feature.GetGeometryRef()
                if geom is None:
                    continue

                # Make valid geometry
                if not geom.IsValid():
                    valid_geom = geom.Buffer(0)  # Simple way to fix self-intersections
                    feature.SetGeometry(valid_geom)
                    layer.SetFeature(feature)

            ds = None
            logger.info(f"Repaired geometries in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error repairing geometries: {str(e)}")
