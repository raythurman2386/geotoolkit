import arcpy
from pathlib import Path
from typing import Union, List, Optional
import re
from ...core.base import BasePreprocessor
from ...core.exceptions import ProcessingError
from ... import setup_logger

logger = setup_logger(
    "arcpy_processor",
    log_level="INFO",
    log_dir=Path(__file__).parent.parent / "logs",
)


class ArcPyPreprocessor(BasePreprocessor):
    """ArcPy implementation of preprocessing operations."""

    def clean_field_names(
        self, dataset: Union[str, Path], exclude_fields: Optional[List[str]] = None
    ) -> Union[str, Path]:
        """
        Clean field names using ArcPy.
        """
        try:
            # Create list of fields to process
            fields = arcpy.ListFields(str(dataset))
            field_mapping = {}

            for field in fields:
                if field.name in ["OBJECTID", "SHAPE", "FID", "Shape"]:
                    continue
                if exclude_fields and field.name in exclude_fields:
                    continue

                # Clean field name
                new_name = re.sub(r"[^a-zA-Z0-9_]", "_", field.name)
                new_name = re.sub(r"_+", "_", new_name)
                new_name = new_name.strip("_").lower()

                if new_name != field.name:
                    field_mapping[field.name] = new_name

            # Rename fields
            for old_name, new_name in field_mapping.items():
                arcpy.AlterField_management(str(dataset), old_name, new_name)

            logger.info(f"Cleaned field names in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error cleaning field names: {str(e)}")

    def standardize_projection(
        self, dataset: Union[str, Path], target_epsg: Union[int, str], in_place: bool = False
    ) -> Union[str, Path]:
        """
        Reproject dataset using ArcPy.
        """
        try:
            arcpy.env.overwriteOutput = True
            input_path = str(dataset)

            # Create spatial reference object
            sr = arcpy.SpatialReference(target_epsg)

            if not in_place:
                # Generate a unique output path
                output_dir = Path(input_path).parent

                # Ensure output filename is valid
                output_name = f"{Path(input_path).stem}_reprojected"
                output_name = re.sub(r"[^a-zA-Z0-9_]", "_", output_name)

                output_path = str(output_dir / output_name)

                # Ensure unique output name
                counter = 1
                while arcpy.Exists(output_path):
                    output_name = re.sub(
                        r"[^a-zA-Z0-9_]", "_", f"{Path(input_path).stem}_reprojected_{counter}"
                    )
                    output_path = str(output_dir / output_name)
                    counter += 1
            else:
                output_path = input_path

            # Create a copy of the input dataset if not in_place
            if not in_place:
                arcpy.CopyFeatures_management(input_path, output_path)

            # Project dataset
            arcpy.Project_management(
                output_path,
                output_path + "_temp",
                sr,
                in_coor_system=arcpy.Describe(output_path).spatialReference,
            )

            # Replace the original with the reprojected data
            arcpy.Delete_management(output_path)
            arcpy.Rename_management(output_path + "_temp", output_path)

            logger.info(f"Reprojected {dataset} to EPSG:{target_epsg}")
            return output_path

        except arcpy.ExecuteError:
            error_message = arcpy.GetMessages(2)
            logger.error(f"ArcPy Error: {error_message}")
            raise ProcessingError(f"Error reprojecting dataset: {error_message}")

        except Exception as e:
            raise ProcessingError(str(e))

    def repair_geometry(
        self, dataset: Union[str, Path], in_place: bool = False
    ) -> Union[str, Path]:
        """
        Fix common geometry errors using ArcPy.
        """
        try:
            input_path = str(dataset)
            if not in_place:
                output_path = str(Path(input_path).with_suffix("")) + "_repaired.shp"
            else:
                output_path = input_path

            # Repair geometry
            arcpy.RepairGeometry_management(input_path, "DELETE_NULL")

            logger.info(f"Repaired geometries in {dataset}")
            return dataset

        except Exception as e:
            raise ProcessingError(f"Error repairing geometries: {str(e)}")
