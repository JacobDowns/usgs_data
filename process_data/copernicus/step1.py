import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
from pyproj import Transformer
from dem_stitcher.stitcher import stitch_dem
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
from pathlib import Path

"""
Downsload Copernicus data.
"""

#data = rioxarray.open_rasterio('data/step1/0.tif')
#plt.imshow(data.data[0])
#plt.show()
#quit()


base_dir = 'data/step2/'

for i in range(1,10):
    base_dir = '/home/jake/usgs/process_data/rgi_indexes/data/step1/'
    index = rioxarray.open_rasterio(f'{base_dir}/RGI_{i}.tif')
        
    src_crs = str(index.rio.crs)
    dst_crs = 'EPSG:4326'
    transformer = Transformer.from_crs(src_crs, dst_crs)

    xx, yy = np.meshgrid(index.x, index.y)
    xs, ys = transformer.transform(xx.flatten(), yy.flatten())
    xmax = xs.max()
    xmin = xs.min()
    ymax = ys.max()
    ymin = ys.min()

    

    dst_area_or_point = 'Point'
    dst_ellipsoidal_height = True
    dem_name = 'glo_30'
    out_directory_name = 'out'
    bounds = [ymin, xmin, ymax, xmax]


    X, p = stitch_dem(
        bounds,
        dem_name=dem_name,
        dst_ellipsoidal_height=dst_ellipsoidal_height,
        dst_area_or_point=dst_area_or_point
    )

    #fig, ax = plt.subplots(figsize=(8, 8))
    #ax = plot.show(X, transform=p['transform'], ax=ax)
    #ax.set_xlabel('Longitude', size=15)
    #ax.set_ylabel('Latitude', size=15)

    height_type = 'ellipsoidal' if dst_ellipsoidal_height else 'geoid'

    with rasterio.open(f'data/step1/{i}.tif', 'w', **p) as ds:
        ds.write(X, 1)
        ds.update_tags(AREA_OR_POINT=dst_area_or_point) 

