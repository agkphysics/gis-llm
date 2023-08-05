import rasterio
from rasterio.mask import mask
from rasterio.plot import show
import fiona
import pandas as pd
import numpy as np

# Open the shapefile
with fiona.open("svi.shp", "r") as shapefile:
    svi_shp = [feature["geometry"] for feature in shapefile if feature['properties']['RPL_THEMES']
>= 0.8]

# Open the raster file
with rasterio.open("raster.tif") as raster:
    out_images, out_transform = mask(raster, svi_shp, crop=True)

# Extract raster values
flood_depths = out_images[0]

row, col = np.nonzero(flood_depths)

# Create data frame of points
points = pd.DataFrame({
    'row': row,
    'col': col,
    'flood_depth': flood_depths
    })

points['coord'] =

# Sorting points by flood depth in descending order and picking top 10
top_points = points.sort_values(by='flood_depth', ascending=False).head(10)

# Extract coordinates of points
coords = top_points['coord'].values

# Printing the coordinates
for point in coords:
    print(f'longitude:{point[0]}, latitude:{point[1]}')
