import rasterio
import rasterio.mask
import fiona
import pandas as pd
import geopandas as gpd
import numpy as np

def query(filename_vector, filename_raster, index_field, value_threshold):
    # Open vector data
    with fiona.open(filename_vector) as vector_data:
        census_tracts = gpd.GeoDataFrame.from_features(vector_data)

    # Open raster data
    with rasterio.open(filename_raster) as raster:
        # Crop raster to census tracts
        cropped_raster, crop_transform = rasterio.mask.mask(raster, census_tracts['geometry'],crop=True)

        # Get statistics for each census tract
        flood_depths = pd.DataFrame.from_records(cropped_raster[0], columns=['flood_depth'])
        flood_depths['geometry'] = census_tracts['geometry']
        flood_depths = gpd.GeoDataFrame(flood_depths)

        # Filter by SVI
        filtered_tracts = flood_depths[flood_depths[index_field] >= value_threshold]

        # Sort by flood depth
        sorted_tracts = filtered_tracts.sort_values('flood_depth', ascending=False)

        # Get top 10 points
        top_points = sorted_tracts.iloc[0:10, :]

        # Transform back to original coordinates
        points = gpd.GeoSeries(top_points['geometry']).to_crs(crop_transform.transform)

        # Return coordinates as a list
        return points.coords.xy[0].tolist()

# Example usage
filename_vector = 'svi_florida.shp'
filename_raster = 'raster.tif'
index_field = 'RPL_THEMES'
value_threshold = 0.8

points = query(filename_vector, filename_raster, index_field, value_threshold)

print(points)
