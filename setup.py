import os
from setuptools import setup, find_packages
from typing import Dict, List


def read_requirements(filename: str) -> List[str]:
    """Read requirements from file and strip comments"""
    with open(filename) as f:
        requirements = []
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements


def get_package_info() -> Dict[str, str]:
    """Get package information from __init__.py"""
    info: Dict[str, str] = {}
    with open(os.path.join('geotoolkit', '__init__.py')) as f:
        for line in f:
            if line.startswith('__'):
                key, value = line.split('=')
                info[key.strip('_ ')] = value.strip('\n "\' ')
    return info


def get_extras_require() -> Dict[str, List[str]]:
    """
    Define extra requirements for different installations.
    Returns a dictionary mapping extra names to their requirements.
    """
    extras_require = {
        # Core geospatial packages
        'core': [
            'gdal>=3.10.0',
            'geopandas>=1.0.1',
            'rasterio>=1.4.3',
            'fiona>=1.10.1',
            'shapely>=2.0.6',
        ],
    }

    # Create 'complete' extra that includes everything
    extras_require['complete'] = [
        req for reqs in extras_require.values() for req in reqs
    ]

    return extras_require


# Get package metadata
package_info = get_package_info()

# Setup configuration
setup(
    name="geotoolkit",
    version=package_info.get('version', '0.1.0'),
    author=package_info.get('author', ''),
    author_email=package_info.get('email', ''),
    description="A comprehensive open-source GIS processing toolkit",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raythurman2386/geotoolkit",
    packages=find_packages(exclude=['tests*', 'docs*']),

    # Python version requirement
    python_requires='>=3.8',

    # Core dependencies (minimal installation)
    install_requires=[
        'gdal>=3.10.0',
        'geopandas>=1.0.1',
        'rasterio>=1.4.3',
        'fiona>=1.10.1',
        'shapely>=2.0.6',
    ],

    # Optional dependencies
    extras_require=get_extras_require(),

    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'geotoolkit=geotoolkit.cli:main',
        ],
    },

    # Package classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],

    # Include non-Python files
    include_package_data=True,
    package_data={
        'geotoolkit': [
            'data/*.json',
            'config/*.yml',
        ],
    },
)