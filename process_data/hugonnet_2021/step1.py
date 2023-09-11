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
Reproject data.
"""

base_dir = '/home/jake/usgs/extracted_data/hugonnet_2021'

def reproject_data(d):
    file_names = glob.glob(f'{base_dir}/{d}/*.tif')
    #print(file_names)


    for file_name in file_names:
        print(file_name)
        name = file_name.split('/')[-1]
        data = rioxarray.open_rasterio(file_name)
        #data.data[np.isnan(data.data)] = 0.
        #plt.imshow(data.data[0])
        #plt.colorbar()
        #plt.show()
    
        data = data.rio.reproject(
            'EPSG:32608',
            resampling=Resampling.bilinear,
            nodata = -9.999e3
        )

        out_dir = f'data/step1/{d}/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        data.rio.to_raster(out_dir + name)
        #plt.imshow(data.data[0])
        #plt.colorbar()
        #plt.show()

reproject_data('2000-2005')
reproject_data('2005-2010')
reproject_data('2010-2015')
reproject_data('2015-2020')
reproject_data('2000-2020')
