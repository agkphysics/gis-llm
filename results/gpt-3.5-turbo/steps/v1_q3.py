import fiona
import rasterio as rio
import rasterio.mask as mask
import pandas as pd
import geopandas as gpd
import numpy as np


def answer():
    # Read the social vulnerability data
    svi_data = gpd.read_file('svi_fl.shp')

    # Filter the data for Miami
    miami_data = svi_data[svi_data['LOCATION'].str.contains('Miami')]

    # Read the flood depth data
    with rio.open('flood_depth_fl.tif') as src:
        # Mask the flood depth data with the Miami data
        miami_masked, _ = rio.mask.mask(src, miami_data.geometry, crop=True)

    # Calculate the average social vulnerability for census tracts with flood depth over 1 foot
    average_vulnerability = np.mean(miami_data[miami_masked > 1]['RPL_THEMES'])

    return {"result": average_vulnerability}


print(answer())
