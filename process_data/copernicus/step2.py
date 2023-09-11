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
from rasterio.enums import Resampling

"""
Downsload Copernicus data.
"""

#data = rioxarray.open_rasterio('data/step1/0.tif')
#plt.imshow(data.data[0])
#plt.show()
#quit()



for i in range(10):
    base_dir = '/home/jake/usgs/process_data/rgi_indexes/data/step1/'
    index = rioxarray.open_rasterio(f'{base_dir}/RGI_{i}.tif')


    data = rioxarray.open_rasterio(f'data/step1/{i}.tif')


    nx, ny = index.data[0].shape
    dst_transform = index.rio.transform()
    
    print(nx, ny)
    print(dst_transform)

    data = data.rio.reproject(
        'EPSG:32608',
        shape=(nx, ny),
        transform=dst_transform,
        resampling=Resampling.bilinear,
        nodata=np.nan,
    )

    out_dir = 'data/step2'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    raster_name = f'{out_dir}/DEM_{i}.tif'
    compress_options = {'compress': 'lzw'} 
    data.rio.to_raster(raster_name, profile=compress_options)
    
    
