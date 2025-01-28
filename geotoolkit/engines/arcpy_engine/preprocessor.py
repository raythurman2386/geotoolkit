import arcpy
from pathlib import Path
from typing import Union, List, Optional
import re
from ...core.base import BasePreprocessor
from ...core.exceptions import ProcessingError
from ... import setup_logger
from ...utils.read_epsg import get_epsg_code

logger = setup_logger(
    "arcpy_processor",
    log_level="INFO",
    log_dir=Path(__file__).parent.parent / "logs",
)


class ArcPyPreprocessor(BasePreprocessor):
    """ArcPy implementation of preprocessing operations."""

    def __init__(self):
        super().__init__()
        self.gdb_name = "arcpy_processing.gdb"
        self.workspace = None
        self.setup_workspace()

    def setup_workspace(self):
        """Set up the geodatabase workspace."""
        try:
            current_dir = Path.cwd()
            self.gdb_path = current_dir / self.gdb_name

            if not self.gdb_path.exists():
                arcpy.management.CreateFileGDB(str(current_dir), self.gdb_name)

            arcpy.env.workspace = str(self.gdb_path)
            arcpy.env.overwriteOutput = True

            logger.info(f"Set up workspace in {self.gdb_path}")
        except Exception as e:
            logger.error(f"Error setting up workspace: {str(e)}")
            raise ProcessingError(f"Error setting up workspace: {str(e)}")

    def _get_output_path(self, input_path: Path, suffix: str) -> Path:
        """Helper method to generate output paths in the geodatabase."""
        output_name = f"{input_path.stem}_{suffix}"
        return self.gdb_path / output_name

    def clean_field_names(
        self, dataset: Union[str, Path], exclude_fields: Optional[List[str]] = None
    ) -> Union[str, Path]:
        """
        Clean field names using ArcPy.
        """
        try:
            input_path = str(dataset)
            fields = arcpy.ListFields(input_path)
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

            if field_mapping:
                output_path = self._get_output_path(Path(dataset), "cleaned")
                arcpy.CopyFeatures_management(input_path, str(output_path))

                # Batch rename fields
                for old_name, new_name in field_mapping.items():
                    arcpy.AlterField_management(str(output_path), old_name, new_name)

                logger.info(f"Cleaned {len(field_mapping)} field names in {output_path}")
                return output_path
            else:
                logger.info("No field names needed cleaning")
                return dataset

        except Exception as e:
            logger.error(f"Error cleaning field names: {str(e)}")
            raise ProcessingError(f"Error cleaning field names: {str(e)}")

    def standardize_projection(
        self, dataset: Union[str, Path], target_epsg: Union[str, int], in_place: bool = False
    ) -> Union[str, Path]:
        try:
            epsg_code = get_epsg_code(target_epsg)
            input_path = Path(dataset)
            output_path = self._get_output_path(input_path, "reprojected")

            # Create spatial reference object
            sr = arcpy.SpatialReference(epsg_code)

            # Project dataset
            arcpy.management.Project(
                in_dataset=str(input_path), out_dataset=str(output_path), out_coor_system=sr
            )

            logger.info(f"Standardized projection to EPSG:{epsg_code} in {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error standardizing projection: {str(e)}")
            raise ProcessingError(f"Error standardizing projection: {str(e)}")

    def repair_geometry(
        self, dataset: Union[str, Path], in_place: bool = False
    ) -> Union[str, Path]:
        try:
            input_path = Path(dataset)
            output_path = self._get_output_path(input_path, "repaired")

            # Copy features to geodatabase
            arcpy.CopyFeatures_management(str(input_path), str(output_path))

            # Repair geometry
            arcpy.RepairGeometry_management(str(output_path), "DELETE_NULL")

            logger.info(f"Repaired geometries in {output_path}")
            return output_path

        except Exception as e:
            raise ProcessingError(f"Error repairing geometries: {str(e)}")
