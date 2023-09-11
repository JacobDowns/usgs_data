import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
from project_mosaic import *


def stitch_rasters(d, field='dhdt'):
    print(d, field)
    src_files = glob.glob(f'data/step1/{d}/*{field}.tif')
    base_dir = '/home/jake/usgs/process_data/rgi_indexes/data/step1/'
    dst_files = [base_dir + 'RGI_{}.tif'.format(i) for i in range(10)]

    out_dir = f'data/step2/{d}'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    out_names = [f'{out_dir}/{field}_{i}.tif' for i in range(10)]
    project_mosaic(src_files, dst_files, out_names)

stitch_rasters('2000-2005')
stitch_rasters('2005-2010')
stitch_rasters('2010-2015')
stitch_rasters('2015-2020')
stitch_rasters('2000-2020')
