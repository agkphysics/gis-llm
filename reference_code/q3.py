import os
import numpy as np

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
selection = svi_layer.getFeatures(QgsFeatureRequest(QgsExpression('"flood_max" > 1')))

social_vul_scores = []
for feature in selection:
    social_vul_scores.append(feature["RPL_THEMES"])

print(
    "Average social vulnerability score of census tracts with max flood depth of greater than 1 ft",
    np.mean(social_vul_scores),
)
