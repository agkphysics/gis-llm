import fiona
import rasterio
import numpy as np
import pandas as pd
from rasterio.mask import mask

# Use Fiona to open the shapefile and get vector data
with fiona.open("svi.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile if feature['properties']['RPL_THEMES']
>= 0.8]

# Use rasterio to open the raster file and get pixel values
with rasterio.open("raster.tif") as src:
    out_image, out_transform = mask(src, shapes, crop=True)
    out_meta = src.meta

data = out_image[0] # get the 2D array data

# Create dataframe with raster data
df_raster = pd.DataFrame(data=np.array(data), columns=['x', 'y', 'value'])

# Sort dataframe by flood depth (value) in descending order and get top 10 highest values
df_raster_sorted = df_raster.sort_values(by='value', ascending=False)
top_10_points = df_raster_sorted.head(10)

# Print coordinates of top 10 highest flood depth points
for i, row in top_10_points.iterrows():
    # convert pixel position to real-world coordinates
    x, y = rasterio.transform.xy(out_transform, row.y, row.x)
    print("Coordinates: ", x, y)
