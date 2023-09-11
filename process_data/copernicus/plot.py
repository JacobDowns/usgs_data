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

base_dir = f'data/step2'

for i in range(10):
    data = rioxarray.open_rasterio(f'{base_dir}/DEM_{i}.tif')
    print(data.x[1] - data.x[0])
    print(data.rio.crs)
    print(data.shape)
    plt.imshow(data[0])
    plt.colorbar()
    plt.show()
