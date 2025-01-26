from geotoolkit import initialize, Preprocessor
from pathlib import Path

initialize(
    preferred_engine='gdal',
    log_level='DEBUG',
    log_dir=Path(__file__).parent / 'logs',
    workspace=Path(__file__).parent / 'workspace'
)

preprocessor = Preprocessor(engine='gdal')
result = preprocessor.clean_field_names("volcanoes.geojson")
projection = preprocessor.standardize_projection(result, "WGS84", False)