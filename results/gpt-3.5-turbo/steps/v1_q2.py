# data_sources: [1,3]


import fiona
import rasterio as rio
import rasterio.mask as mask
import pandas as pd
import geopandas as gpd
import numpy as np

def answer():
    # Read the social vulnerability data
    svi_data = gpd.read_file('svi_fl.shp')

    # Filter the data to include only tracts with a social vulnerability index of 0.8 or greater
    svi_data_filtered = svi_data[svi_data['RPL_THEMES'] >= 0.8]

    # Read the flood depth data
    flood_depth_data = rio.open('flood_depth_fl.tif')

    # Create an empty dictionary to store the maximum predicted flood depth for each tract
    max_flood_depth = {}

    # Iterate over each tract in the filtered social vulnerability data
    for index, tract in svi_data_filtered.iterrows():
        # Get the geometry of the tract
        tract_geometry = tract.geometry

        # Mask the flood depth data with the tract geometry
        masked_data, _ = mask.mask(flood_depth_data, [tract_geometry], crop=True)

        # Get the maximum flood depth value for the masked data
        max_depth = np.max(masked_data)

        # Store the maximum flood depth value for the tract
        max_flood_depth[tract['ID']] = max_depth

    return {"result": max_flood_depth}
