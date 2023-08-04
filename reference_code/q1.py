import fiona
import numpy as np
import pandas as pd
import rasterio
import rasterio.mask

# select features (census tracts) by attribute and write to new shapefile
print("Selecting features by attribute...")
with fiona.open("svi_florida.shp") as input:
    relevant_features = []
    for feature in input:
        if feature["properties"]["RPL_THEMES"] >= 0.8:
            relevant_features.append(feature)

# use selected features to clip raster
print("Clipping raster...")
shapes = [feature["geometry"] for feature in relevant_features]
with rasterio.open("raster.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
out_meta.update(
    {
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform,
        "compress": "deflate",
    }
)

# output_raster_path = "raster2.tif"
# with rasterio.open(output_raster_path, "w", **out_meta) as dest:
#     dest.write(out_image)

print("Finding top 10 flood depth values...")
band_id = 1

# raster = rasterio.open(output_raster_path)
# band_arr = raster.read(band_id)
band_arr = out_image[band_id - 1]

# create list of all raster pixel value and coordinates
idxs = np.argsort(band_arr, axis=None)
top_10_idxs = idxs[-10:]
x, y = np.unravel_index(top_10_idxs, band_arr.shape)
top_10_vals = band_arr[x, y]
x, y = rasterio.transform.xy(out_transform, x, y)
print(list(zip(x, y, top_10_vals)))

# px_vals = []
# for x in range(band_arr.shape[0]):
#     for y in range(band_arr.shape[1]):
#         px_vals.append({"x": x, "y": y, "value": band_arr[x, y]})

# # select and print top 10 flood depth values with clipped raster
# df = pd.DataFrame.from_records(px_vals)
# print(df.sort_values("value", ascending=False).head(10))
