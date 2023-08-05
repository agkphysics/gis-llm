def answer():
    import fiona
    import rasterio
    import rasterio.mask
    import pandas as pd
    import geopandas as gpd
    import numpy as np

    # Read the shapefile
    shapefile = gpd.read_file('svi.shp')

    # Read the raster file
    raster = rasterio.open('raster.tif')

    # Crop the raster to the extent of the shapefile
    cropped_raster, _ = rasterio.mask.mask(raster, shapefile.geometry, crop=True)

    # Get the flood depths as a numpy array
    flood_depths = cropped_raster[0]

    # Get the SVI values as a numpy array
    svi_values = shapefile['RPL_THEMES'].values

    # Get the indices of census tracts with SVI >= 0.8
    svi_indices = np.where(svi_values >= 0.8)[0]

    # Get the indices of the 10 highest flood depths
    flood_indices = np.argsort(flood_depths, axis=None)[-10:]

    # Get the coordinates of the points with the 10 highest flood depths in census tracts with SVI >= 0.8
    coordinates = []
    for i in flood_indices:
        row, col = np.unravel_index(i, flood_depths.shape)
        coordinates.append((raster.bounds.left + col * raster.res[0], raster.bounds.top - row * raster.res[1]))

    return {'coordinates': coordinates}
