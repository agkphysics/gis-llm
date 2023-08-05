import fiona
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gpd
import numpy as np

# Read shapefile
shapefile = gpd.read_file('svi_florida.shp')

# Read raster file
raster = rasterio.open('raster.tif')

# Crop raster to relevant polygons
clipped_raster, _ = rasterio.mask.mask(raster, shapefile.geometry, crop=True)

# Flatten raster data
flatten_raster = clipped_raster.flatten()

# Find indices of points with highest flood depths
top_indices = np.argpartition(flatten_raster, -10)[-10:]

# Filter shapefile based on SVI
filtered_shapefile = shapefile[shapefile['RPL_THEMES'] >= 0.8]

# Get coordinates of points with highest flood depths
coordinates = filtered_shapefile.geometry.apply(lambda g: g.centroid).iloc[top_indices].apply(lambda p: (p.x, p.y))

coordinates
print(coordinates)
