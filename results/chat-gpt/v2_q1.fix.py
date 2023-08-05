import fiona
import rasterio
from rasterio import mask
import pandas as pd
import numpy as np

# Define the paths to the shapefile and raster file
shapefile_path = 'svi_florida.shp'
raster_path = 'raster.tif'

# Open the shapefile using fiona
shapefile = fiona.open(shapefile_path, 'r')

# Read the raster file using rasterio
raster = rasterio.open(raster_path)

# Create an empty DataFrame to store the coordinates and flood depths
data = pd.DataFrame(columns=['Latitude', 'Longitude', 'FloodDepth'])

# Iterate over the shapefile features
for feature in shapefile:
    # Get the SVI value from the 'RPL_THEMES' field
    svi_value = feature['properties']['RPL_THEMES']

    # Check if SVI is 0.8 or greater
    if svi_value >= 0.8:
        # Extract the geometry of the feature
        geometry = feature['geometry']

        # Mask the raster data using the feature's geometry
        masked_data, _ = mask.mask(raster, [geometry], crop=False)

        # Get the flood depths within the masked region
        flood_depths = masked_data[0]

        # Find the indices of the top 10 flood depths
        top_10_indices = np.unravel_index(np.argsort(flood_depths, axis=None)[-10:], flood_depths.shape)

        # Extract the coordinates and flood depths of the top 10 points
        top_10_coordinates = raster.xy(*top_10_indices)
        top_10_flood_depths = flood_depths[top_10_indices]

        # Add the coordinates and flood depths to the DataFrame
        data = pd.concat([data, pd.DataFrame({'Latitude': top_10_coordinates[0],
                                              'Longitude': top_10_coordinates[1],
                                              'FloodDepth': top_10_flood_depths})], ignore_index=True)

# Sort the DataFrame by flood depth in descending order
data = data.sort_values('FloodDepth', ascending=False)

# Display the top 10 points
top_10_points = data.head(10)
print(top_10_points)
