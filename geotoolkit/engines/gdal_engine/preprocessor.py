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
    "gdal_processor",
    log_level="INFO",
    log_dir=Path(__file__).parent.parent / "logs",
)


class GDALPreprocessor(BasePreprocessor):
    """GDAL implementation of preprocessing operations."""

    def __init__(self):
        gdal.UseExceptions()
        self.spatial_ref = SpatialReference()

    def clean_field_names(
        self, dataset: Union[str, Path], exclude_fields: Optional[List[str]] = None
    ) -> Union[str, Path]:
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
                new_name = re.sub(r"[^a-zA-Z0-9_]", "_", old_name)
                new_name = re.sub(r"_+", "_", new_name)  # Remove multiple underscores
                new_name = new_name.strip("_").lower()

                if new_name != old_name:
                    field_mapping[old_name] = new_name

            # Rename fields
            for old_name, new_name in field_mapping.items():
                layer.AlterFieldDefn(
                    layer_defn.GetFieldIndex(old_name),
                    ogr.FieldDefn(
                        new_name,
                        layer_defn.GetFieldDefn(layer_defn.GetFieldIndex(old_name)).GetType(),
                    ),
                    ogr.ALTER_NAME_FLAG,
                )

            ds = None  # Close dataset
            logger.info(f"Cleaned field names in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error cleaning field names: {str(e)}")

    def standardize_projection(
        self, dataset: Union[str, Path], target_epsg: Union[str, int], in_place: bool = False
    ):
        """
        Standardize the projection of a dataset to a specified coordinate system.

        Args:
            dataset: Path to input dataset
            target_epsg: EPSG code or string identifier for the target coordinate system
            in_place: Whether to modify the input dataset or create a new one

        Returns:
            Path to processed dataset
        """
        try:
            epsg_code = get_epsg_code(target_epsg)
            input_path = Path(dataset)

            if in_place:
                output_path = input_path
            else:
                output_path = input_path.with_name(
                    f"{input_path.stem}_reprojected{input_path.suffix}"
                )

            # Open the input dataset
            ds = ogr.Open(str(input_path), 0)
            if ds is None:
                raise ProcessingError(f"Could not open dataset: {dataset}")

            # Create the output dataset
            driver = ogr.GetDriverByName(ds.GetDriver().GetName())
            out_ds = driver.CreateDataSource(str(output_path))

            # Create the target spatial reference
            target_srs = osr.SpatialReference()
            target_srs.ImportFromEPSG(epsg_code)

            # Process each layer
            for layer in ds:
                source_srs = layer.GetSpatialRef()

                if source_srs is None:
                    logger.warning(f"Source layer has no defined CRS. Assuming EPSG:{epsg_code}")
                    source_srs = target_srs

                # Create coordinate transformation
                transform = osr.CoordinateTransformation(source_srs, target_srs)

                # Create the output layer
                out_layer = out_ds.CreateLayer(layer.GetName(), target_srs, layer.GetGeomType())
                layer_defn = layer.GetLayerDefn()

                # Copy field definitions
                for i in range(layer_defn.GetFieldCount()):
                    out_layer.CreateField(layer_defn.GetFieldDefn(i))

                # Process features
                for feature in layer:
                    geom = feature.GetGeometryRef()
                    if geom is not None:
                        geom.Transform(transform)

                    out_feature = ogr.Feature(out_layer.GetLayerDefn())
                    out_feature.SetGeometry(geom)

                    # Copy attributes
                    for i in range(layer_defn.GetFieldCount()):
                        out_feature.SetField(
                            layer_defn.GetFieldDefn(i).GetNameRef(), feature.GetField(i)
                        )

                    out_layer.CreateFeature(out_feature)
                    out_feature = None

            ds = None
            out_ds = None

            logger.info(f"Standardized projection to EPSG:{epsg_code} in {output_path}")
            return output_path

        except Exception as e:
            raise ProcessingError(f"Error standardizing projection: {str(e)}")

    def repair_geometry(
        self, dataset: Union[str, Path], in_place: bool = False
    ) -> Union[str, Path]:
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

    def ensure_2d_geometry(
        self, dataset: Union[str, Path], in_place: bool = False
    ) -> Union[str, Path]:
        """
        Ensure all geometries in the dataset are 2D.

        Args:
            dataset: Path to input dataset
            in_place: Whether to modify the input dataset or create a new one

        Returns:
            Path to processed dataset
        """
        try:
            input_path = Path(dataset)
            if not in_place:
                output_path = input_path.with_name(f"{input_path.stem}_2d{input_path.suffix}")
            else:
                output_path = input_path

            ds = ogr.Open(str(input_path), 0)
            if ds is None:
                raise ProcessingError(f"Could not open dataset: {dataset}")

            driver = ogr.GetDriverByName(ds.GetDriver().GetName())
            out_ds = driver.CreateDataSource(str(output_path))

            for layer in ds:
                out_layer = out_ds.CreateLayer(
                    layer.GetName(), layer.GetSpatialRef(), layer.GetGeomType()
                )
                layer_defn = layer.GetLayerDefn()

                # Copy field definitions
                for i in range(layer_defn.GetFieldCount()):
                    out_layer.CreateField(layer_defn.GetFieldDefn(i))

                # Process features
                for feature in layer:
                    geom = feature.GetGeometryRef()
                    if geom is not None:
                        geom = ogr.ForceToLineString(geom)

                    out_feature = ogr.Feature(out_layer.GetLayerDefn())
                    out_feature.SetGeometry(geom)

                    # Copy attributes
                    for i in range(layer_defn.GetFieldCount()):
                        out_feature.SetField(
                            layer_defn.GetFieldDefn(i).GetNameRef(), feature.GetField(i)
                        )

                    out_layer.CreateFeature(out_feature)
                    out_feature = None

            ds = None
            out_ds = None

            logger.info(f"Ensured 2D geometries in {output_path}")
            return output_path

        except Exception as e:
            raise ProcessingError(f"Error ensuring 2D geometries: {str(e)}")

    def calculate_sinuosity(self, dataset: Union[str, Path], field_name: str):
        """
        Calculate sinuosity for line geometries in the dataset.
        """
        try:
            ds = ogr.Open(str(dataset), 1)  # Open for writing
            if ds is None:
                raise ProcessingError(f"Could not open dataset: {dataset}")

            layer = ds.GetLayer()
            srs = layer.GetSpatialRef()
            epsg_code = srs.GetAuthorityCode(None)
            logger.info(f"Calculating sinuosity with EPSG:{epsg_code}")

            # Add the field for sinuosity values if it doesn't exist
            if layer.FindFieldIndex(field_name, 1) == -1:
                field_defn = ogr.FieldDefn(field_name, ogr.OFTReal)
                layer.CreateField(field_defn)

            for feature in layer:
                geom = feature.GetGeometryRef()
                if geom is None or geom.GetGeometryType() != ogr.wkbLineString:
                    continue

                # Compute actual path length
                path_length = geom.Length()

                # Compute straight-line distance (start -> end)
                start_point = geom.GetPoint(0)  # (x, y, z)
                end_point = geom.GetPoint(geom.GetPointCount() - 1)

                straight_distance = ((start_point[0] - end_point[0]) ** 2 +
                                     (start_point[1] - end_point[1]) ** 2) ** 0.5

                # Calculate sinuosity (handling division by zero)
                if straight_distance > 0:
                    sinuosity = path_length / straight_distance
                else:
                    sinuosity = 1  # Undefined, default to 1

                feature.SetField(field_name, sinuosity)
                layer.SetFeature(feature)

            ds = None  # Close dataset
            logger.info(f"Calculated sinuosity for {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error calculating sinuosity: {str(e)}")
