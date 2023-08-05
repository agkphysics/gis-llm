import numpy as np
from qgis.core import QgsRasterLayer, QgsVectorLayer

# Path to the shapefile and raster file
shapefile_path = 'svi.shp'
raster_path = 'raster.tif'

# Load the vector layer (shapefile)
vector_layer = QgsVectorLayer(shapefile_path, 'svi', 'ogr')
if not vector_layer.isValid():
    print("Vector layer failed to load!")

# Load the raster layer
raster_layer = QgsRasterLayer(raster_path, 'raster')
if not raster_layer.isValid():
    print("Raster layer failed to load!")

# Set up a dictionary to store the maximum flood depth for each census tract
max_depths = {}

# Iterate over each feature in the vector layer
for feature in vector_layer.getFeatures():
    svi_value = feature['RPL_THEMES']

    # Check if the SVI value is 0.8 or greater
    if svi_value >= 0.8:
        # Get the geometry of the feature
        geometry = feature.geometry()

        # Clip the raster layer to the extent of the feature's geometry
        clipped_raster = raster_layer.clip(geometry)

        # Convert the clipped raster to a numpy array
        raster_array = clipped_raster.dataProvider().block(1, clipped_raster.extent(), clipped_raster.width(), clipped_raster.height())

        # Find the maximum value in the raster array
        max_depth = np.nanmax(raster_array)

        # Store the maximum depth for the current census tract
        max_depths[feature.id()] = max_depth

# Print the maximum flood depth for each census tract
for tract_id, max_depth in max_depths.items():
    print(f"Census Tract {tract_id}: {max_depth} meters")
