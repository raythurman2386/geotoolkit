from geotoolkit import initialize
from pathlib import Path

# Initialize the toolkit
initialize(
    preferred_engine='gdal',
    log_level='DEBUG',
    log_dir=Path('logs'),
    workspace=Path('workspace')
)

# Your processing code here...