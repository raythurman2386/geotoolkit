# GeoToolKit

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/geotoolkit/badge/?version=latest)](https://geotoolkit.readthedocs.io/en/latest/?badge=latest)

GeoToolKit is a comprehensive Python package that provides a unified interface for common GIS operations using both ArcPy and GDAL/Open Source implementations. It aims to simplify geospatial workflows while maintaining flexibility in choosing the underlying GIS engine.

## 🚀 Features

- **Dual Engine Support**: Seamlessly switch between ArcPy and GDAL implementations
- **Automated Engine Detection**: Automatically selects available GIS engine
- **Comprehensive Tools**:
    - Data Preprocessing
    - Spatial Analysis
    - Raster Processing
    - Quality Control
    - Batch Processing
    - Data Integration

## 📋 Requirements

### Minimum Requirements
- Python 3.8+
- GDAL 3.0+ (for GDAL engine)
- ArcGIS Pro 2.5+ (for ArcPy engine)

### Optional Dependencies
- NumPy
- Pandas
- GeoPandas
- Rasterio

## ⚡️ Quick Installation

```bash
# Basic installation with GDAL support
pip install geotoolkit

# Full installation with all optional dependencies
pip install geotoolkit[all]

# ArcPy-only installation
pip install geotoolkit[arcpy]
```

## 🎯 Usage Examples

### Basic Usage

```python
from geotoolkit import Preprocessor, Analyzer, RasterTools

# Initialize with automatic engine detection
preprocessor = Preprocessor()

# Or specify your preferred engine
preprocessor = Preprocessor(engine='gdal')

# Clean field names in a dataset
preprocessor.clean_field_names("input_data.shp")

# Perform spatial analysis
analyzer = Analyzer()
results = analyzer.calculate_statistics("analysis_layer.shp")
```

### Engine Selection

```python
from geotoolkit.utils.config import ConfigManager

# Configure default engine
config = ConfigManager()
config.update_config(
    preferred_engine='gdal',
    max_threads=8,
    workspace='/path/to/workspace'
)
```

## 🏗️ Project Structure

```
geotoolkit/
├── core/           # Core functionality and abstractions
├── engines/        # Engine-specific implementations
├── interfaces/     # User-facing interfaces
├── utils/          # Utility functions and helpers
├── tests/          # Test suite
└── examples/       # Usage examples and notebooks
```

## 🔧 Configuration

GeoToolKit can be configured through the `ConfigManager`:

```python
from geotoolkit.utils.config import ConfigManager

config = ConfigManager()
config.update_config(
    preferred_engine='gdal',  # 'gdal', 'arcpy', or 'auto'
    max_threads=4,
    log_level='INFO',
    workspace='/path/to/workspace'
)
```

## 📚 Documentation

Comprehensive documentation is available at [readthedocs.io](https://geotoolkit.readthedocs.io/).

- [User Guide](https://geotoolkit.readthedocs.io/en/latest/user_guide.html)
- [API Reference](https://geotoolkit.readthedocs.io/en/latest/api.html)
- [Examples](https://geotoolkit.readthedocs.io/en/latest/examples.html)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_gdal/
pytest tests/test_arcpy/
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/geotoolkit.git
cd geotoolkit

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [ ] Add support for cloud-based GIS services
- [ ] Implement machine learning integration
- [ ] Add support for real-time data processing
- [ ] Develop web service capabilities
- [ ] Create GUI interface

## 📫 Contact

- Project Maintainer: [Your Name](mailto:raymondthurman5@gmail.com)
- Project Homepage: https://github.com/raythurman2386/geotoolkit

## 🙏 Acknowledgments

- GDAL/OGR contributors
- Esri and ArcPy development team
- Open source GIS community

---

Made with ❤️ by [Ray Thurman]