# Installation Guide

## Requirements

### Minimum Requirements
- Python 3.10+
- GDAL 3.0+ (for GDAL engine)
- ArcGIS Pro 2.5+ (for ArcPy engine)

### Optional Dependencies
- NumPy
- Pandas
- GeoPandas
- Rasterio

## Installation Methods

### Basic Installation
For basic installation with GDAL support:

```bash
pip install geotoolkit
```

### Full Installation
To install with all optional dependencies:

```bash
pip install geotoolkit[all]
```

### ArcPy-only Installation
If you only need ArcPy functionality:

```bash
pip install geotoolkit[arcpy]
```

!!! note "Installation Note"
    The current install process is under development and may require some attention. For the most reliable setup, follow the development setup process described below.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/raythurman2386/geotoolkit.git
   cd geotoolkit
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Troubleshooting

If you encounter any installation issues, please check the following:

1. Ensure your Python version is 3.10 or higher
2. For GDAL users, verify GDAL is properly installed on your system
3. For ArcPy users, ensure ArcGIS Pro is installed and the Python environment is properly configured
