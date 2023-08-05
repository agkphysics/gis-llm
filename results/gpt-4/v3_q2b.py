# load the vector and raster layers
vector_layer = QgsVectorLayer('svi.shp', 'svi', 'ogr')
raster_layer = QgsRasterLayer('raster.tif', 'raster')
QgsProject.instance().addMapLayer(vector_layer)
QgsProject.instance().addMapLayer(raster_layer)

# select the polygons with a social vulnerability index of 0.8 or greater
expression = QgsExpression('"RPL_THEMES" >= 0.8')
request = QgsFeatureRequest(expression)
selected_features = vector_layer.getFeatures(request)

# prepare the output
output = {}

# process each selected census tract
for feature in selected_features:

    # crop the raster to the current polygon
    x_min, y_min, x_max, y_max = feature.geometry().boundingBox().asWktPolygon()
    processing.run("gdal:cliprasterbyextent",
        {'INPUT':raster_layer,
         'PROJWIN':f"{x_min},{x_max},{y_min},{y_max}",
         'OUTPUT':'temp.tif'})

    # load the cropped raster
    clipped_raster = QgsRasterLayer('temp.tif', 'temp')

    # calculate the maximum flood depth
    stats = clipped_raster.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
    max_depth = stats.maximumValue

    # store the result
    output[feature['RPL_THEMES']] = max_depth

# print the output
for svi, max_depth in output.items():
    print(f"SVI: {svi}, Max flood depth: {max_depth}")
