layer = QgsVectorLayer('svi.shp', 'svi', 'ogr')
raster_path = 'raster.tif'
polygon_raster_clip_path = 'clip.tif'

processing.run("native:extractbymask", {
    'MASK': layer,
    'INPUT': raster_path,
    'OUTPUT': polygon_raster_clip_path
})

clip_layer = QgsRasterLayer(polygon_raster_clip_path, "clip")
provider = clip_layer.dataProvider()
ext = provider.extent()
rows = clip_layer.height()
cols = clip_layer.width()
block = provider.block(1, ext, cols, rows)

features = layer.getFeatures()
for feature in features:
    if feature['RPL_THEMES'] >= 0.8:
        geom = feature.geometry()
        xmin, ymin, xmax, ymax = geom.boundingBox().toRectF().getCoords()

        xmin = int((xmin - ext.xMinimum()) / clip_layer.rasterUnitsPerPixelX())
        xmax = int((xmax - ext.xMinimum()) / clip_layer.rasterUnitsPerPixelX())
        ymin = int((ext.yMaximum() - ymin) / clip_layer.rasterUnitsPerPixelY())
        ymax = int((ext.yMaximum() - ymax) / clip_layer.rasterUnitsPerPixelY())

        max_value = np.amax(block.read(xmin, ymin, xmax - xmin, ymax - ymin))
        print('Census Tract:', feature['FID'], 'Max Flood Depth:', max_value)
