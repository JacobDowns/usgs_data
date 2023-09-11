import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
from project_mosaic import *

"""
Set nan data. 
"""

base_dir = 'data/step2/'

def replace_nan(year, field = 'v_err'):
    print(year, field)

    file_names = glob.glob(f'data/step2/{field}_{year}*.tif')
    for file_name in file_names:

        name = file_name.split('/')[-1]
        tile = int(name.split('.')[0].split('_')[-1])

        base_dir = '/media/storage/usgs_data/process_data/rgi_indexes/data/step1/'
        index = rioxarray.open_rasterio(f'{base_dir}/RGI_{tile}.tif')

        v = rioxarray.open_rasterio(file_name)
        v.data[v.data <= 0.] = np.nan
        v.data[0][index.data[0] == 0] = np.nan
        #plt.imshow(v[0], vmax=50.)
        #plt.show()

        out_dir = f'data/step3/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        out_file = f'{out_dir}/{name}'
        print(out_file)
        v.rio.to_raster(out_file, nodata = np.nan)

for year in range(1985,2019):
    replace_nan(str(year))
