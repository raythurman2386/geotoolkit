import os
from pathlib import Path
from typing import Union, List, Optional
from osgeo import gdal, ogr, osr
import re
from ...core.base import BasePreprocessor
from ...core.exceptions import ProcessingError
from ... import logger


class GDALPreprocessor(BasePreprocessor):
    """GDAL implementation of preprocessing operations."""

    def __init__(self):
        gdal.UseExceptions()  # Enable exception handling

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

    def standardize_projection(self, dataset: Union[str, Path],
                               target_epsg: Union[int, str],
                               in_place: bool = False) -> Union[str, Path]:
        """
        Reproject dataset using GDAL.
        
        Args:
            dataset: Path to input dataset
            target_epsg: Target EPSG code
            in_place: Whether to modify the input dataset or create new one
            
        Returns:
            Path to processed dataset
        """
        try:
            # Create output path if not in_place
            input_path = str(dataset)
            if not in_place:
                output_path = str(Path(input_path).with_suffix('')) + '_reprojected.shp'
            else:
                output_path = input_path

            # Open input
            ds = ogr.Open(input_path)
            if ds is None:
                raise ProcessingError(f"Could not open dataset: {input_path}")

            # Get input spatial reference
            layer = ds.GetLayer()
            source_srs = layer.GetSpatialRef()

            # Create target spatial reference
            target_srs = osr.SpatialReference()
            if isinstance(target_epsg, int):
                target_srs.ImportFromEPSG(target_epsg)
            else:
                target_srs.ImportFromWkt(target_epsg)

            # Create coordinate transformation
            transform = osr.CoordinateTransformation(source_srs, target_srs)

            # Create output dataset
            driver = ogr.GetDriverByName("ESRI Shapefile")
            if not in_place:
                if os.path.exists(output_path):
                    driver.DeleteDataSource(output_path)
                out_ds = driver.CreateDataSource(output_path)

                # Create output layer
                out_layer = out_ds.CreateLayer(
                    layer.GetName(),
                    target_srs,
                    layer.GetGeomType()
                )

                # Copy fields
                layer_defn = layer.GetLayerDefn()
                for i in range(layer_defn.GetFieldCount()):
                    out_layer.CreateField(layer_defn.GetFieldDefn(i))

                # Process features
                for feature in layer:
                    geom = feature.GetGeometryRef()
                    geom.Transform(transform)

                    out_feature = ogr.Feature(out_layer.GetLayerDefn())
                    out_feature.SetGeometry(geom)

                    for i in range(layer_defn.GetFieldCount()):
                        out_feature.SetField(i, feature.GetField(i))

                    out_layer.CreateFeature(out_feature)
                    out_feature = None

                out_ds = None
                ds = None

            logger.info(f"Reprojected {dataset} to EPSG:{target_epsg}")
            return output_path

        except Exception as e:
            raise ProcessingError(f"Error reprojecting dataset: {str(e)}")

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
