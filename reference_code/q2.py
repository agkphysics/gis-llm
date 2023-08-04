import os

from qgis.analysis import QgsZonalStatistics
from qgis.core import (
    QgsExpression,
    QgsFeatureRequest,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
)

# Load the census tract polygons with social vulnerability index
svi_layer = QgsVectorLayer("svi.shp", "zonepolygons", "ogr")

# Load the raster with flood depths
raster_layer = QgsRasterLayer("raster.tif")

# Calculate zonal statistics within each polygon (mean, max, min)
zone_stat = QgsZonalStatistics(
    svi_layer,
    raster_layer,
    attributePrefix="flood_",
    rasterBand=1,
    stats=QgsZonalStatistics.Mean | QgsZonalStatistics.Max | QgsZonalStatistics.Min,
)
zone_stat.calculateStatistics(None)
# svi_layer.commitChanges()

# Select census tracts and print max flood depth
selection = svi_layer.getFeatures(QgsFeatureRequest(QgsExpression('"RPL_THEMES" > 0.8')))
for feature in selection:
    if isinstance(feature["flood_max"], float):
        print(feature["LOCATION"], "max flood depth", feature["flood_max"])
