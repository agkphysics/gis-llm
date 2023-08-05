from qgis.analysis import QgsZonalStatistics
from qgis.core import QgsRasterLayer, QgsVectorLayer

# load vector layer
vector_path = 'svi.shp'
vector_layer = QgsVectorLayer(vector_path, 'census_tracts', 'ogr')

# Select only polygons with an SVI of 0.8 and above
expr = "RPL_THEMES >= 0.8"
vector_layer.selectByExpression(expr, QgsVectorLayer.SetSelection)

# load raster layer
raster_path = 'raster.tif'
raster_layer = QgsRasterLayer(raster_path, 'flood_depths')

# perform zonal statistics
zoneStat = QgsZonalStatistics(vector_layer, raster_layer, 'prefix_', 1,
QgsZonalStatistics.Max)
zoneStat.calculateStatistics(None)

# print max flood depth for each tract
for feature in vector_layer.selectedFeatures():
    max_flood_depth = feature['prefix_max']
    print(f"Flood depth: {max_flood_depth}")
