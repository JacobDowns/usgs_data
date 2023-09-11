import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
from rasterio.enums import Resampling

"""
Reproject data.
"""

base_dir = '/media/new/usgs_data/extracted_data/ITS_LIVE/'

def reproject_data(year, field='vy'):
    print(year, field)
    file_names = glob.glob(f'{base_dir}/ALA_G0240_{year}_{field}.tif')

    for file_name in file_names:
        print(file_name)
        name = file_name.split('/')[-1]
        data = rioxarray.open_rasterio(file_name)
        #data.data[0][data.data[0] < 0.] = 0.

        #plt.imshow(data.data[0])
        #plt.colorbar()
        #plt.show()
  
    
        data = data.rio.reproject(
            'EPSG:32608',
            resampling=Resampling.bilinear,
            resolution=100.,
            nodata=0.
        )

        out_dir = f'data/step1/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        print(data.rio)
        #quit()
        data.rio.to_raster(out_dir + name)
        #plt.imshow(data.data[0])
        #plt.colorbar()
        #plt.show()

for year in range(1985, 2019):
    reproject_data(str(year))
#reproject_data('2005-2010')
#reproject_data('2010-2015')
#reproject_data('2015-2020')
#reproject_data('2000-2020')
