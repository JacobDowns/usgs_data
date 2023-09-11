import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import pandas as pd
from project_mosaic import *

def stitch_rasters(year, field='vy'):
    print(year, field)
    src_files = glob.glob(f'data/step1/ALA_G0240_{year}_{field}.tif')
    base_dir = '/media/new/usgs_data/process_data/rgi_indexes/data/step1/'
    dst_files = [base_dir + 'RGI_{}.tif'.format(i) for i in range(10)]

    out_dir = f'data/step2'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    out_names = [f'{out_dir}/{field}_{year}_{i}.tif' for i in range(10)]
    project_mosaic(src_files, dst_files, out_names)

for year in range(1985, 2019):
    stitch_rasters(str(year))
