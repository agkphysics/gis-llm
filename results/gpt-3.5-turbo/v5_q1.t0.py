import fiona
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gpd
import numpy as np

# Read the shapefile
shapefile = gpd.read_file('svi.shp')

# Read the raster file
raster = rasterio.open('raster.tif')

# Crop the raster to the extent of the shapefile
raster_crop, raster_transform = rasterio.mask.mask(raster, shapefile.geometry, crop=True)

# Get the flood depths as a numpy array
flood_depths = raster_crop[0]

# Get the indices of the 10 highest flood depths
top_10_indices = np.unravel_index(np.argsort(flood_depths, axis=None)[-10:], flood_depths.shape)

# Get the coordinates of the points with the 10 highest flood depths
top_10_coordinates = rasterio.transform.xy(raster_transform, top_10_indices[0], top_10_indices[1])

# Filter the shapefile to census tracts with a social vulnerability index of 0.8 or greater
filtered_shapefile = shapefile[shapefile['RPL_THEMES'] >= 0.8]

# Get the coordinates of the filtered census tracts
filtered_coordinates = filtered_shapefile.geometry.centroid

# Find the intersection of the top 10 coordinates and the filtered coordinates
intersection_coordinates = set(top_10_coordinates).intersection(filtered_coordinates)

# Print the coordinates of the points with the 10 highest flood depths in census tracts with a social vulnerability index of 0.8 or greater
for coordinate in intersection_coordinates:
    print(coordinate)
