import requests
from osgeo import gdal
import numpy as np

gdal.UseExceptions()


def calculate_pixel_size(bbox, target_resolution):
    """
    Calculate the appropriate pixel size based on the desired resolution.
    """
    min_long, min_lat, max_long, max_lat = bbox
    meters_per_degree = 111319.9  # at the equator
    latitude_factor = np.cos(np.radians(min_lat))
    width_meters = abs(max_long - min_long) * meters_per_degree * latitude_factor
    height_meters = abs(max_lat - min_lat) * meters_per_degree
    width_pixels = int(width_meters / target_resolution)
    height_pixels = int(height_meters / target_resolution)
    width_pixels = max(width_pixels, 100)
    height_pixels = max(height_pixels, 100)

    return width_pixels, height_pixels


def download_ned_tile(bbox, output_tif_path, resolution=10):
    """
    Download NED tile within the specified bounding box and save it to a TIFF file.
    """
    min_long, min_lat, max_long, max_lat = bbox

    # Calculate appropriate pixel dimensions
    width_pixels, height_pixels = calculate_pixel_size(bbox, resolution)

    print(f"""
    Downloading DEM for area:
    Southwest corner: ({min_long}, {min_lat})
    Northeast corner: ({max_long}, {max_lat})
    Target resolution: {resolution} meters
    Image dimensions: {width_pixels}x{height_pixels} pixels
    """)

    # Use the higher resolution 3DEP service
    url = "https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer/exportImage"

    params = {
        "bbox": f"{min_long},{min_lat},{max_long},{max_lat}",
        "bboxSR": 4326,
        "size": f"{width_pixels},{height_pixels}",
        "imageSR": 4326,
        "format": "tiff",
        "pixelType": "F32",
        "noDataInterpretation": "esriNoDataMatchAny",
        "interpolation": "RSP_BilinearInterpolation",
        "f": "image"
    }

    try:
        response = requests.get(url, params=params, stream=True)
        response.raise_for_status()

        with open(output_tif_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded tile to {output_tif_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return False


def verify_dem(tif_file_path):
    """
    Verify the downloaded DEM file and print statistics.
    """
    try:
        ds = gdal.Open(tif_file_path)
        if ds is None:
            print("Failed to open the DEM file")
            return False

        # Get raster band
        band = ds.GetRasterBand(1)

        # Read data into numpy array
        data = band.ReadAsArray()

        # Get geotransform information
        geotransform = ds.GetGeoTransform()

        # Print detailed information
        print("\nDEM Information:")
        print(f"Dimensions: {ds.RasterXSize} x {ds.RasterYSize} pixels")
        print(f"Projection: {ds.GetProjection()}")
        print(f"Pixel Size: {geotransform[1]:.8f}, {geotransform[5]:.8f}")

        print("\nElevation Statistics:")
        print(f"Min elevation: {np.min(data):.2f} meters")
        print(f"Max elevation: {np.max(data):.2f} meters")
        print(f"Mean elevation: {np.mean(data):.2f} meters")
        print(f"Standard deviation: {np.std(data):.2f} meters")

        # Check for no data values
        no_data_value = band.GetNoDataValue()
        if no_data_value is not None:
            no_data_count = np.sum(data == no_data_value)
            print(f"No data value: {no_data_value}")
            print(f"Number of no data pixels: {no_data_count}")

        ds = None  # Close the dataset
        return True

    except Exception as e:
        print(f"Error verifying DEM: {e}")
        return False


def main():
    southwest_corner = (-95.7647365, 34.0552608)
    northeast_corner = (-95.7304076, 34.0695508)

    bbox = (
        southwest_corner[0],  # min_longitude
        southwest_corner[1],  # min_latitude
        northeast_corner[0],  # max_longitude
        northeast_corner[1]  # max_latitude
    )

    # Download at different resolutions
    resolutions = [10, 30]  # Add or remove resolutions as needed

    for resolution in resolutions:
        output_tif_path = f"output_dem_{resolution}m.tif"

        print(f"\nDownloading {resolution}-meter resolution DEM...")
        if download_ned_tile(bbox, output_tif_path, resolution=resolution):
            if verify_dem(output_tif_path):
                print(f"\n{resolution}m DEM processing completed successfully!")
            else:
                print(f"\n{resolution}m DEM verification failed!")
        else:
            print(f"\nFailed to download {resolution}m DEM data!")


if __name__ == "__main__":
    main()
