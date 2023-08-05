import numpy as np
from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer, QgsZonalStatistics

# Load the vector layer (shapefile)
vector_layer = QgsVectorLayer('svi.shp', 'svi', 'ogr')
if not vector_layer.isValid():
    print('Invalid vector layer')
    exit(1)

# Load the raster layer
raster_layer = QgsRasterLayer('raster.tif', 'raster')
if not raster_layer.isValid():
    print('Invalid raster layer')
    exit(1)

# Set the extent of the raster layer to match the vector layer
extent = vector_layer.extent()
raster_layer.setExtent(extent)
raster_layer.triggerRepaint()

# Add the layers to the QGIS project
project = QgsProject.instance()
project.addMapLayer(vector_layer)
project.addMapLayer(raster_layer)

# Initialize the zonal statistics object
zonal_stats = QgsZonalStatistics(vector_layer, raster_layer)

# Define the field name for the SVI
svi_field_name = 'RPL_THEMES'

# Filter the census tracts based on the social vulnerability index
expression = QgsExpression(svi_field_name + ' >= 0.8')
request = QgsFeatureRequest(expression)
features = vector_layer.getFeatures(request)

# Iterate over the filtered features and calculate the maximum flood depth for each census tract
for feature in features:
    svi_value = feature[svi_field_name]
    rect = feature.geometry().boundingBox()
    stats = zonal_stats.calculateStatistics(rect, QgsZonalStatistics.Maximum)
    max_depth = stats[1]  # index 1 corresponds to the maximum value
    print(f"Census Tract: {feature.id()} | SVI: {svi_value} | Max Flood Depth: {max_depth:.2f} meters")

# Remove the layers from the project (optional)
project.removeMapLayer(vector_layer.id())
project.removeMapLayer(raster_layer.id())
