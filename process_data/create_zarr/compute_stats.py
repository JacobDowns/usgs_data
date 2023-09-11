import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import geopandas as gp
import glob
from multiprocessing import Pool

file_names = glob.glob('glaciers.zarr/*')
rgi_ids = [f.split('/')[-1] for f in file_names]

def get_stats(rgi_id):
    print(rgi_id)

    store = xr.open_zarr(f'glaciers.zarr/{rgi_id}')
    x = store['x'].data
    y = store['y'].data
    z = store['dem'].data
    mask = store['mask'].data
    #print(mask)
    H = store['H_millan'].data
    dhdt = store['dhdt_2000-2020'].data

    H[mask == 0.] = np.nan
    z[mask == 0.] = np.nan
    dhdt[mask == 0.] = np.nan

    d = {}
    d['RGIId'] = rgi_id
    d['area'] = (mask*100.*100 / 1e6).sum()
    d['H_avg'] = np.nanmean(H)
    d['H_med'] = np.nanmedian(H)
    d['z_avg'] = np.nanmean(z)
    d['z_med'] = np.nanmedian(z)
    d['dhdt_avg'] = np.nanmean(dhdt)
    d['dhdt_med'] = np.nanmedian(dhdt)

    return d

pool = Pool(processes=12)
results = pool.map(get_stats, rgi_ids)
df = pd.DataFrame(results)
df = df.set_index('RGIId')
df = df.sort_values(by=['RGIId'])
df = df.round(3)
df.to_csv('stats.csv')
print(df)

