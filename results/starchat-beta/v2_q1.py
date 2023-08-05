import rasterio
import fiona
import pandas as pd
import numpy as np

# Open the raster dataset
with rasterio.open("raster.tif") as dataset:
    # Crop the raster dataset to the relevant region
    raster_crop = dataset.read(1, masked=True).clip(svi_geometry)

# Load the social vulnerability index data from the shapefile
with fiona.open("svi.shp") as svi_source:
    svi_features = [feature for feature in svi_source if "RPL_THEMES" in feature['properties']]
    svi_data = pd.DataFrame.from_records(svi_features)

# Filter the svi data to tracts with a social vulnerability index of 0.8 or higher
svi_high = svi_data[svi_data["RPL_THEMES"] >= 0.8]

# Group the svi data by census tract and calculate the mean flood depth
svi_grouped = svi_high.groupby(" Geometry").mean()["raster_crop"]

# Get the coordinates of the points with the 10 highest flood depths
top_10_floods = svi_grouped.sort_values(ascending=False)[:10].index

# Get the coordinates of the points in a list
flood_coords = [geometry.coords[0] for geometry in top_10_floods]
