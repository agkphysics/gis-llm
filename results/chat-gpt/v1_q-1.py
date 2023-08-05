import rasterio
from rasterio import mask
import fiona
import pandas as pd

# Read the shapefile
shapefile_path = 'svi.shp'
with fiona.open(shapefile_path, 'r') as shapefile:
    features = [feature for feature in shapefile]

# Read the raster data
raster_path = 'raster.tif'
with rasterio.open(raster_path) as src:
    # Crop the raster to the extent of the shapefile polygons
    out_image, out_transform = rasterio.mask.mask(src, [feature['geometry'] for feature in features], crop=True)
    out_meta = src.meta

# Update metadata to reflect the cropped extent
out_meta.update({'height': out_image.shape[1], 'width': out_image.shape[2], 'transform': out_transform})

# Mask the cropped raster with the shapefile polygons
masked_data = out_image[0]

# Extract the flood depths and SVI values for each polygon
flood_depths = []
svi_values = []
for feature in features:
    geometry = feature['geometry']
    svi = feature['properties']['RPL_THEMES']
    # Get the mask of the polygon
    mask_poly = mask.geometry_mask([geometry], out_shape=masked_data.shape, transform=out_transform, invert=True)
    # Calculate the maximum flood depth within the polygon
    max_depth = masked_data[mask_poly].max()
    flood_depths.append(max_depth)
    svi_values.append(svi)

# Create a dataframe with flood depths and SVI values
data = {'Flood_Depth': flood_depths, 'SVI': svi_values}
df = pd.DataFrame(data)

# Filter the polygons based on the social vulnerability index (SVI) threshold
threshold = 0.8
filtered_df = df[df['SVI'] >= threshold]

# Sort the filtered polygons by flood depths in descending order
sorted_df = filtered_df.sort_values(by='Flood_Depth', ascending=False)

# Retrieve the coordinates of the top 10 polygons
top_10_polygons = sorted_df.head(10)
top_10_coordinates = []
with fiona.open(shapefile_path, 'r') as shapefile:
    for feature in shapefile:
        if feature['properties']['RPL_THEMES'] in top_10_polygons['SVI'].values:
            geometry = feature['geometry']
            centroid = shape(feature['geometry']).centroid
            top_10_coordinates.append((centroid.x, centroid.y))

print("Coordinates of the 10 census tracts with a social vulnerability index of 0.8 or greater with the highest flood depths:")
for i, coord in enumerate(top_10_coordinates):
    print(f"Polygon {i+1}: {coord}")
