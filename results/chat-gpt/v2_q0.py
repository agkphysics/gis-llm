import rasterio
import fiona
import pandas as pd
from rasterio.mask import mask

# Open the shapefile
shapefile_path = "svi.shp"
shapefile = fiona.open(shapefile_path)

# Open the raster file
raster_path = "raster.tif"
raster = rasterio.open(raster_path)

# Create an empty dataframe to store the results
results_df = pd.DataFrame(columns=["Polygon", "Coordinates", "Flood Depth"])

# Iterate over each feature (census tract) in the shapefile
for feature in shapefile:
    # Get the SVI value for the current feature
    svi_value = feature["properties"]["RPL_THEMES"]

    # Check if SVI is greater than or equal to 0.8
    if svi_value >= 0.8:
        # Get the geometry of the current feature
        geometry = feature["geometry"]

        # Mask the raster with the current feature's geometry
        masked_data, masked_transform = mask(raster, [geometry], crop=True)

        # Get the maximum flood depth within the masked region
        max_depth = masked_data.max()

        # Get the coordinates of the maximum flood depth within the masked region
        max_depth_coords = list(zip(*np.where(masked_data == max_depth)))

        # Add the results to the dataframe
        results_df = results_df.append({
            "Polygon": feature["id"],
            "Coordinates": max_depth_coords,
            "Flood Depth": max_depth
        }, ignore_index=True)

# Sort the dataframe by flood depth in descending order
results_df = results_df.sort_values(by="Flood Depth", ascending=False)

# Get the top 10 results
top_10_results = results_df.head(10)

# Print the coordinates and flood depths of the top 10 results
for _, row in top_10_results.iterrows():
    print(f"Polygon {row['Polygon']}:")
    print("Coordinates:", row["Coordinates"])
    print("Flood Depth:", row["Flood Depth"])
    print()

# Close the shapefile and raster file
shapefile.close()
raster.close()
