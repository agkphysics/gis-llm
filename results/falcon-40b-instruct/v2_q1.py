import rasterio
import fiona
import pandas as pd
import numpy as np

# Set the path to the rasterawk module and the script to generate the raster
rasterawk_path = '~/workspace/rasterawk'
generate_script_path = '~/workspace/flood/raster_generator.awk'

# Generate the raster
subprocess.call(['{} {}'.format(rasterawk_path, generate_script_path)], shell=True)

# Import the raster data
raster = rasterio.open('raster.tif')

# Import the shapefile data
with fiona.open('svi.shp') as source:
    data = {
        record['properties'][key]: record[key]
        for key, record in source.iter_features()
    }

# Create a DataFrame from the shapefile data
df = pd.DataFrame(data)

# Add the social vulnerability index to the DataFrame
df['RPL_THEMES'] = df.RPL_THEMES.map({
    'Low': 0.0,
    'Medium': 0.8 - 0.1,
    'High': 1.0
})

# Crop the raster to the bounds of the shapefile data
raster = raster.clip(box=df.geometry.total_bounds)

# Extract the flood depth statistics for each census tract
flood_depth_data = pd.DataFrame(raster.get_statistic('max').astype(int)).reset_index()
flood_depth_data.columns = ['flood_depth_max']

# Join the raster and shapefile data on the census tract ID
flood_depth_df = pd.merge(df, flood_depth_data, left_on='SHAPE.id', right_index=True, how='left')

# Filter the DataFrame to keep only census tracts with a social vulnerability index of at least 0.8
flood_depth_df = flood_depth_df.loc[flood_depth_df['RPL_THEMES'] >= 0.8]

# Reorder the DataFrame columns to match the desired format
flood_depth_data = flood_depth_df.drop(['RPL_THEMES', 'SHAPE.id'], axis=1).sort_values('geometry.y').reset_index()

# Extract the coordinates of the points with the top 10 flood depths
