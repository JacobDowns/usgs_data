import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
from compute_indexes import *

"""
Downsample velocity and thickness data.
"""


base_dir = '/home/jake/usgs/process_data/millan_2022/data/step1/'
file_names = [base_dir + f'V_{i}.tif' for i in range(10)]
out_names = ['data/step1/RGI_{}.tif'.format(i) for i in range(10)]

print(file_names)
print(out_names)
write_index_rasters(file_names, out_names)

