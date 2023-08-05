import fiona
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gpd
import numpy as np

# Open the shapefile and read the data
with fiona.open("svi.shp") as svi_src:
    svi_data = pd.DataFrame.from_records(svi_src)

# Open the raster file and read the data
with rasterio.open("raster.tif") as raster_src:
    raster_data = raster_src.read()

# Clip the raster data to the SVI polygons
svi_mask = svi_data["RPL_THEMES"] >= 0.8
raster_clip, _ = rasterio.mask.mask(raster_src, svi_mask.values, crop=True)

# Get the coordinates of the points with the 10 highest flood depths
flood_points = raster_clip[0].flatten()
top_10_floods = np.argsort(flood_points)[-10:]
top_10_points = [raster_src.xy(r, c) for r, c in zip(*top_10_floods)]

# Convert the points to a GeoDataFrame
points_df = gpd.GeoDataFrame(pd.DataFrame(top_10_points, columns=["y", "x"]), crs=raster_src.crs)

# Print the coordinates
print(points_df.to_wkt())
