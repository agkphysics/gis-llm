# Load the necessary layers
svi_layer = QgsVectorLayer('svi.shp', 'svi', 'ogr')
flood_depth_layer = QgsRasterLayer('raster.tif', 'flood_depth')

# Check if the layers are loaded successfully
if not svi_layer.isValid() or not flood_depth_layer.isValid():
    print("Failed to load one or more layers.")
    exit()

# Create a list to store the maximum flood depths
max_flood_depths = []

# Iterate over each feature in the SVI layer
for feature in svi_layer.getFeatures():
    svi_value = feature['RPL_THEMES']

    # Check if the SVI value is 0.8 or greater
    if svi_value >= 0.8:
        # Get the geometry of the feature
        geometry = feature.geometry()

        # Crop the flood depth raster to the extent of the feature's geometry
        cropped_raster = QgsRasterCalculatorEntry()
        cropped_raster.raster = flood_depth_layer
        cropped_raster.ref = 'raster@1'
        cropped_raster.bandNumber = 1
        cropped_raster.extent = geometry.boundingBox()

        # Set up the raster calculator expression to get the maximum flood depth
        expression = 'maximum(raster@1)'
        entries = [cropped_raster]

        # Perform the raster calculation
        calculator = QgsRasterCalculator(expression, '/tmp/output.tif', 'GTiff', cropped_raster.extent, cropped_raster.width, cropped_raster.height, entries)
        calculator.processCalculation()

        # Read the maximum flood depth from the output raster
        output_raster = QgsRasterLayer('/tmp/output.tif', 'output')
        provider = output_raster.dataProvider()
        block = provider.block(1, output_raster.extent(), output_raster.width(), output_raster.height())
        max_depth = np.nanmax(block.data)

        # Store the maximum flood depth in the list
        max_flood_depths.append(max_depth)

# Print the maximum flood depth for each census tract
for i, feature in enumerate(svi_layer.getFeatures()):
    svi_value = feature['RPL_THEMES']

    if svi_value >= 0.8:
        census_tract = feature['TRACT']
        print(f"Census Tract {census_tract}: {max_flood_depths[i]} meters")

# Remove the temporary output raster file
QgsProject.instance().removeMapLayer(output_raster)
