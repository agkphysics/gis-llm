import pandas, geopandas, rasterio, rasterio.mask, numpy, fiona

## Inserted code



shapefile = geopandas.read_file('svi.shp')
raster = rasterio.open('raster.tif')

# Filter shapefile data for high SVI tracts
high_svi_tracts = shapefile[shapefile['RPL_THEMES'] >= 0.8]

# Mask raster data to high SVI tracts
mask, transform = rasterio.mask.mask(raster, high_svi_tracts.geometry, crop=True)

# Retrieve the indices for the top 10 flood depths
indices_1d = mask.ravel().argsort()[-10:]
idx = numpy.unravel_index(indices_1d, mask.shape)

# Retrieve the top 10 flood depth coordinates
coordinates = raster.transform * (idx[1] + 0.5, idx[0] + 0.5)

coordinates.tolist()


print(coordinates.tolist())
