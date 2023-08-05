import fiona
import rasterio
from rasterio import mask
import pandas as pd

# Open the shapefile and raster file
shapefile_path = 'svi_florida.shp'
raster_path = 'raster.tif'

# Read the shapefile and extract the features with SVI >= 0.8
svi_threshold = 0.8
with fiona.open(shapefile_path, 'r') as shapefile:
    features = [feature for feature in shapefile if feature['properties']['RPL_THEMES'] >= svi_threshold]

# Read the raster file and crop it to the extent of the selected features
with rasterio.open(raster_path) as src:
    out_image, out_transform = mask.mask(src, [feature['geometry'] for feature in features], crop=True)
    out_meta = src.meta.copy()

# Extract the flood depths and corresponding coordinates
flood_depths = out_image[0]
rows, cols = flood_depths.shape
transform = out_transform

coordinates = []
for feature in features:
    coords = feature['geometry']['coordinates']
    min_row, min_col = rasterio.transform.rowcol(transform, coords[0][0][0], coords[0][0][1])
    max_row, max_col = rasterio.transform.rowcol(transform, coords[0][2][0], coords[0][2][1])
    coordinates.append((min_col, min_row, max_col, max_row))

# Create a pandas dataframe to store the results
data = {'Coordinates': coordinates, 'Flood Depth': flood_depths.flatten()}
df = pd.DataFrame(data)

# Sort the dataframe by SVI in descending order and flood depths in descending order
df = df.sort_values(by=['Flood Depth'], ascending=False)

# Print the top 10 coordinates with the highest flood depths and SVI >= 0.8
top_10_coordinates = df.head(10)['Coordinates']
print(top_10_coordinates)
