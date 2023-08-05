import fiona, rasterio, rasterio.mask, numpy


def answer():
    with fiona.open('svi.shp', 'r') as shapefile:
        polygons = [feature["geometry"] for feature in shapefile if feature['properties']['RPL_THEMES'] >= 0.8]

    with rasterio.open('raster.tif') as src:
        out_image, out_transform = rasterio.mask.mask(src, polygons, crop=True)
        out_meta = src.meta.copy()

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    flood_depths = out_image.flatten()
    flood_depths_sorted_indices = numpy.argsort(flood_depths)[::-1]
    top_10_flood_depths_indices = flood_depths_sorted_indices[:10]

    top_10_flood_depths_coords = []
    for index in top_10_flood_depths_indices:
        row, col = numpy.unravel_index(index, out_image.shape)
        x, y = rasterio.transform.xy(out_transform, row, col)
        top_10_flood_depths_coords.append((x, y))

    return {'coordinates': top_10_flood_depths_coords}
