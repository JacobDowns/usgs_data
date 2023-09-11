import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import rioxarray

"""
Plot reprojected data.
"""

base_dir = f'data/step1'
"""
fields = ['V', 'H', 'VX_STD', 'VY_STD']

for i in range(6,9):
    for field in fields:
        print(i, field)
        data = rioxarray.open_rasterio(f'{base_dir}/{field}_{i}.tif')
        print(data.rio.crs)
        print(data.shape)
    print()
""" 

field = 'V'

for i in range(9):
    data = rioxarray.open_rasterio(f'{base_dir}/{field}_{i}.tif')
    print(data.x[1] - data.x[0])
    print(data.rio.crs)
    print(data.shape)
    plt.imshow(data[0])
    plt.colorbar()
    plt.show()
