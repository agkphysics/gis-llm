import fiona
import rasterio
from rasterio import mask
import pandas as pd
import numpy as np

# Read the census tracts shapefile
shapefile = 'svi.shp'
with fiona.open(shapefile, "r") as shapefile:
    features = [feature for feature in shapefile]

# Read the raster data
rasterfile = 'raster.tif'
with rasterio.open(rasterfile) as src:
    raster_data = src.read(1)
    transform = src.transform

# Crop the raster data to the extent of the census tracts
census_tract_geometries = [feature["geometry"] for feature in features]
masked_raster, masked_transform = mask.mask(src, census_tract_geometries, crop=True)
masked_raster = masked_raster[0]

# Create a dataframe to hold the flood depths and their coordinates
df = pd.DataFrame({
    'flood_depth': masked_raster.flatten(),
    'x': np.repeat(np.arange(masked_raster.shape[1]) * masked_transform[0] + masked_transform[2], masked_raster.shape[0]),
    'y': np.tile(np.arange(masked_raster.shape[0]) * masked_transform[4] + masked_transform[5], masked_raster.shape[1])
})

# Filter the dataframe for census tracts with a social vulnerability index of 0.8 or greater
svi_threshold = 0.8
filtered_df = df[df['RPL_THEMES'] >= svi_threshold]

# Get the coordinates of the points with the 10 highest flood depths
top_10_points = filtered_df.nlargest(10, 'flood_depth')[['x', 'y']]

print(top_10_points)
