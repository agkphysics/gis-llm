layer = QgsVectorLayer('svi.shp', 'svi', 'ogr')
svi_field_index = layer.fields().indexFromName('RPL_THEMES')
layer.selectByExpression('"RPL_THEMES" >= 0.8')
ids = [feat.id() for feat in layer.getSelectedFeatures()]
layer.removeSelection()

raster_layer = QgsRasterLayer('raster.tif', 'raster')
features = [feat for feat in layer.getFeatures() if feat.id() in ids]
stats = []
for feat in features:
    geom = feat.geometry().boundingBox()
    xmin, ymin, xmax, ymax = geom.xMinimum(), geom.yMinimum(), geom.xMaximum(), geom.yMaximum()
    extent = QgsRectangle(xmin, ymin, xmax, ymax)
    provider = raster_layer.dataProvider()
    stats.append(provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0))

max_depths = [stat.maximumValue for stat in stats]
max_depths
