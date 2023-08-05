# data_sources: [1,3]

import fiona
import rasterio as rio
import rasterio.mask
import pandas as pd
import geopandas as gpd
import numpy as np


def answer():
    # Load the shapefile using geopandas
    svi_fl = gpd.read_file('svi_fl.shp')

    # Filter the data to only include census tracts with a social vulnerability index of 0.8 or greater
    svi_fl = svi_fl[svi_fl['RPL_THEMES'] >= 0.8]

    # Load the raster file using rasterio
    with rio.open('flood_depth_fl.tif') as flood_depth_fl:
        # Create an empty dictionary to store the results
        result = {}

        # Loop over each row in the filtered shapefile
        for index, row in svi_fl.iterrows():
            # Create a mask for the current census tract
            mask = [row.geometry.__geo_interface__]

            # Apply the mask to the raster data
            out_image, out_transform = rasterio.mask.mask(flood_depth_fl, mask, crop=True)

            # Find the maximum flood depth in the masked data
            max_flood_depth = np.nanmax(out_image)

            # Add the maximum flood depth to the results dictionary, using the census tract information as the key
            result[row['LOCATION']] = max_flood_depth

    return {"result": result}


##
print(answer())
