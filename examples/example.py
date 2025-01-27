from geotoolkit import initialize, Preprocessor
from pathlib import Path

initialize(
    preferred_engine='gdal',
    log_level='DEBUG',
    log_dir=Path(__file__).parent / 'logs',
    workspace=Path(__file__).parent / 'workspace'
)

preprocessor = Preprocessor(engine='gdal')
file = "route_66.shp"
result = preprocessor.clean_field_names(file)
projection = preprocessor.standardize_projection(result, 4326, False)
geometry = preprocessor.repair_geometry(projection, False)
correct_geom = preprocessor.ensure_2d_geometry(geometry, False)