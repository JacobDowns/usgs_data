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

d = '2000-2005'
base_dir = f'data/step3'
field = 'dhdt'

for i in range(9):
    data = rioxarray.open_rasterio(f'{base_dir}/{d}/{field}_{i}.tif')
    print(data.x[1] - data.x[0])
    print(data.rio.crs)
    print(data.shape)
    plt.imshow(data[0], vmin=-20, vmax=20.)
    plt.colorbar()
    plt.show()
