import fiona, rasterio, rasterio.mask, numpy, geopandas, pandas as pd


def answer():
    # Load the shapefile
    with fiona.open('svi_fl.shp', 'r') as shapefile:
        shapes = [feature["geometry"] for feature in shapefile if feature['properties']['RPL_THEMES'] >= 0.8]

    # Load the raster and mask it with the shapefile
    with rasterio.open('raster.tif') as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta.copy()

    # Create a dataframe from the masked raster
    df = pd.DataFrame(out_image.reshape(-1, out_image.shape[-1]), columns=['flood_depth'])

    # Create a geopandas dataframe from the shapefile
    gdf = geopandas.read_file('svi_fl.shp')
    gdf = gdf[gdf['RPL_THEMES'] >= 0.8]

    # Calculate the maximum flood depth for each census tract
    max_flood_depths = df.groupby(gdf.index).max()

    # Return the result as a dictionary
    return max_flood_depths.to_dict()


print(answer())
