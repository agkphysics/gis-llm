from qgis.analysis import QgsZonalStatistics
from qgis.core import QgsVectorLayer, QgsRasterLayer
from PyQt5.QtCore import QVariant

# Load Census Tracts Layer
census_tracts = QgsVectorLayer('svi.shp', 'censustracts', 'ogr')

# Load Flood Depths Raster Layer
flood_depths = QgsRasterLayer('raster.tif', 'flooddepths')

# Filter Census Tracts with RPL_THEMES >= 0.8
request = QgsFeatureRequest().setFilterExpression('"RPL_THEMES" >= 0.8')
filtered_tracts =

# Create a new layer that includes only the polygons with RPL_THEMES >= 0.8
vlayer = QgsVectorLayer("Polygon", "filtered_tracts", "memory")
pr = vlayer.dataProvider()

# Add the same fields of the original layer to the new layer
for f in census_tracts.fields():
    pr.addAttributes()
vlayer.updateFields()

# Add the features to the new layer
for f in filtered_tracts:
    pr.addFeatures()
vlayer.updateExtents()

# Add the new attribute for Max Flood Depth
vlayer.dataProvider().addAttributes([QgsField("Max_Flood_Depth", QVariant.Double)])
vlayer.updateFields()

# Perform Zonal Statistics and get the maximum value of the raster for each feature in the vector layer
zs = QgsZonalStatistics(vlayer, flood_depths, 'Max_Flood_Depth_', 1, QgsZonalStatistics.Max)
zs.calculateStatistics(None)

# Print the maximum flood depths for each filtered census tract
for feature in vlayer.getFeatures():
    print(f"Census tract ID: {feature.id()}, Maximum Flood Depth: {feature['Max_Flood_Depth_']}")
