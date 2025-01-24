# 1. Simple usage with default engine
from geotoolkit import initialize, Preprocessor

initialize()
preprocessor = Preprocessor()
result = preprocessor.clean_field_names("input.shp")

# 2. Switching engines temporarily
from geotoolkit import GeoToolKitContext

with GeoToolKitContext(engine='arcpy'):
    preprocessor = Preprocessor()
    arcpy_result = preprocessor.clean_field_names("input.shp")

# 3. Using multiple engines
from geotoolkit import PreprocessorFactory

gdal_prep = PreprocessorFactory.create('gdal')
arcpy_prep = PreprocessorFactory.create('arcpy')

# 4. Configuration-based usage
from geotoolkit import initialize
from pathlib import Path

initialize(
    preferred_engine='gdal',
    log_level='DEBUG',
    log_dir=Path('logs'),
    workspace=Path('workspace')
)

# 5. Advanced usage with custom settings
from geotoolkit.utils.config import ConfigManager

config = ConfigManager()
config.update_config(
    preferred_engine='gdal',
    max_threads=4,
    chunk_size=1000
)

preprocessor = Preprocessor()
preprocessor.clean_field_names("input.shp", chunk_size=config.config.chunk_size)