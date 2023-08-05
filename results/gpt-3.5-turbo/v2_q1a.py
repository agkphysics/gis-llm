import fiona
import rasterio
import pandas as pd
import numpy as np
from rasterio import mask

# Load the shapefile
with fiona.open('svi.shp') as shp:
    features = [feature["geometry"] for feature in shp]

# Load the raster file
with rasterio.open('raster.tif') as src:
    raster = src.read(1)
    transform = src.transform

# Convert the shapefile features to raster shape
shapes = [feature["geometry"] for feature in fiona.open('svi.shp')]

# Mask the raster with the shapefile
out_image, out_transform = mask.mask(raster, shapes, crop=True)
out_meta = src.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

# Iterate through the masked raster to get the flood depths
flood_depths = out_image.flatten()
flood_depths = np.ma.compressed(flood_depths)

# Filter the raster based on SVI
with fiona.open('svi.shp') as shp:
    data = np.array([float(feature["properties"]["RPL_THEMES"]) for feature in shp])
    filtered_flood_depths = flood_depths[data >= 0.8]

# Get the indices and coordinates of the 10 highest flood depths
top_10_indices = np.argpartition(filtered_flood_depths, -10)[-10:]
top_10_coordinates = []
for i in top_10_indices:
    row, col = np.where(out_image == filtered_flood_depths[i])
    px, py = rasterio.transform.xy(out_transform, row, col)
    top_10_coordinates.append((px[0], py[0]))

# Print the coordinates of the points with the 10 highest flood depths
for coordinate in top_10_coordinates:
    print(coordinate)
