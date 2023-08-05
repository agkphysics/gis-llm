import fiona
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gpd
import numpy as np

# Open the shapefile and read the data
with fiona.open("svi_fl.shp") as svi_src:
    svi_data = pd.DataFrame.from_records(svi_src)

# Open the raster file and read the data
with rasterio.open("flood_depth_fl.tif") as raster_src:
    raster_data = raster_src.read()

# Clip the raster data to the SVI polygons
svi_mask = svi_data["RPL_THEMES"] >= 0.8
raster_masked = rasterio.mask.mask(raster_data, [svi_mask.values], crop=True)

# Get the coordinates of the points with the 10 highest flood depths
points = gpd.GeoDataFrame.from_features(svi_src)
points_masked = gpd.GeoDataFrame(raster_masked[0], crs=raster_src.crs, geometry=points.geometry)
points_sorted = points_masked.sort_values(by=raster_src.name, ascending=False)
top_10 = points_sorted.head(10)

# Print the coordinates
for index, row in top_10.iterrows():
    print(row.geometry.coords[0])
