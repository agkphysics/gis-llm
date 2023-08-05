def answer():
    import fiona
    import rasterio
    import rasterio.mask
    import pandas as pd
    import geopandas as gpd
    import numpy as np

    # Read the shapefile
    shapefile = gpd.read_file('svi_fl.shp')

    # Filter the shapefile to include only census tracts in Florida with SVI >= 0.8
    florida_tracts = shapefile[(shapefile['STATE'] == 'FL') & (shapefile['RPL_THEMES'] >= 0.8)]

    # Read the raster file
    raster = rasterio.open('raster.tif')

    # Crop the raster to the extent of the filtered shapefile
    cropped_raster, _ = rasterio.mask.mask(raster, florida_tracts.geometry, crop=True)

    # Calculate the maximum flood depth for each census tract
    max_depths = np.nanmax(cropped_raster, axis=1)

    # Create a dataframe with the census tract IDs and maximum flood depths
    result_df = pd.DataFrame({'Census Tract': florida_tracts['TRACTCE'], 'Max Flood Depth': max_depths})

    # Convert the dataframe to a dictionary
    result_dict = result_df.set_index('Census Tract').to_dict()['Max Flood Depth']

    return result_dict


print(answer())
