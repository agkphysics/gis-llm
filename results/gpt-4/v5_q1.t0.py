import pandas, geopandas, rasterio, rasterio.mask, numpy, fiona

## Inserted code



# Load the shapefile
svi_gdf = geopandas.read_file('svi_florida.shp')

# Filter the shapefile for polygons with SVI of 0.8 or greater
svi_gdf = svi_gdf[svi_gdf['RPL_THEMES'] >= 0.8]

# Load the raster file
with rasterio.open('raster.tif') as src:
    # Crop the raster data to the relevant polygons
    out_image, out_transform = rasterio.mask.mask(src, svi_gdf.geometry, crop=True)
    out_meta = src.meta.copy()

# Update the metadata with the new cropped raster data
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

# Create a DataFrame from the raster data
raster_df = pandas.DataFrame(out_image[0])

# Flatten the DataFrame and sort by flood depth
raster_df = raster_df.stack().reset_index()
raster_df.columns = ['y', 'x', 'flood_depth']
raster_df = raster_df.sort_values('flood_depth', ascending=False)

# Get the coordinates of the points with the 10 highest flood depths
top_10_flood_depths = raster_df.head(10)

# Convert pixel coordinates to map coordinates
top_10_flood_depths['x'] = top_10_flood_depths['x'] * out_transform[0] + out_transform[2]
top_10_flood_depths['y'] = top_10_flood_depths['y'] * out_transform[4] + out_transform[5]

top_10_flood_depths[['x', 'y']]


print(top_10_flood_depths[['x', 'y']])
