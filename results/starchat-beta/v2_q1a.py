import rasterio
import fiona
import numpy as np
import pandas as pd

# Open the SVI shapefile
svi_src = fiona.open("svi.shp")
svi_df = pd.DataFrame.from_records(svi_src)

# Open the raster file
with rasterio.open("raster.tif") as raster_src:
    # Crop the raster to the extent of the SVI polygons
    crop_window = raster_src.window(*svi_src.bbox)
    crop_arr = rasterio.mask.crop(raster_src, crop_window=crop_window)

    # Calculate the SVI for each polygon
    svi = np.mean(crop_arr["RPL_THEMES"])

# Filter the SVI dataframe to only include polygons with an SVI of 0.8 or greater
high_svi_df = svi_df[svi_df["RPL_THEMES"] >= 0.8]

# Create a new dataframe with the filtered SVI polygons
filt_df = pd.merge(high_svi_df, crop_arr, left_index=True, right_index=True)

# Sort the dataframe by flood depth and select the top 10
sorted_df = filt_df.sort_values("RPL_THEMES", ascending=False)
top_10_df = sorted_df.head(10)

# Extract the coordinates from the top 10 dataframe
coords = top_10_df.geometry.tolist()
