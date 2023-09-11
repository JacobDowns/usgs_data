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
Reproject Farinotti data.
"""

base_dir = 'data/step2/'

def replace_nan(d, field = 'dhdt_err'):
    print(d, field)

    for i in range(10):
        base_dir = '/media/storage/usgs_data/process_data/rgi_indexes/data/step1/'
        index = rioxarray.open_rasterio(f'{base_dir}/RGI_{i}.tif')
        
    
        dhdt = rioxarray.open_rasterio(f'data/step2/{d}/{field}_{i}.tif')
        dhdt.data[dhdt.data < -250.] = np.nan
        dhdt.data[0][index.data[0] == 0] = np.nan

    
        #plt.imshow(dhdt.data[0], vmin = -20., vmax=20.)
        #plt.colorbar()
        #plt.show()

        out_dir = f'data/step3/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        out_file = f'{out_dir}/{field}_{d}_{i}.tif'.format(i)
        dhdt.rio.to_raster(out_file, nodata = np.nan)

replace_nan('2000-2005')
replace_nan('2005-2010')
replace_nan('2010-2015')
replace_nan('2015-2020')
replace_nan('2000-2020')
