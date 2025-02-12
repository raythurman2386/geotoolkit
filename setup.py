from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="geotoolkit",
    packages=find_packages(),
    version="0.1.0",
    description="A collection of tools for geospatial analysis",
    author="Ray Thurman",
    license="MIT",
    install_requires=requirements,
)
