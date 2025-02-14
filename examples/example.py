from pathlib import Path

from geotoolkit import Preprocessor, initialize

initialize(
    preferred_engine="auto",
    log_level="DEBUG",
    log_dir=Path(__file__).parent / "logs",
    workspace=Path(__file__).parent / "workspace",
)

# preprocessor = Preprocessor(engine="gdal")
file = "./examples/route_66.shp"
# result = preprocessor.clean_field_names(file)
# projection = preprocessor.standardize_projection(result, 4326, False)
# geometry = preprocessor.repair_geometry(projection, False)
# correct_geom = preprocessor.ensure_2d_geometry(geometry, False)
# sinuosity = preprocessor.calculate_sinuosity(correct_geom, "sinuosity")

arcpy_preprocessor = Preprocessor(engine="arcpy")
arcpy_result = arcpy_preprocessor.clean_field_names(file)
arcpy_projection = arcpy_preprocessor.standardize_projection(arcpy_result, 4326)
arcpy_repair = arcpy_preprocessor.repair_geometry(arcpy_result, False)
arcpy_sinuosity = arcpy_preprocessor.calculate_sinuosity(arcpy_repair, "sinuosity")
