import numpy as np
import rioxarray
import xarray
import matplotlib.pyplot as plt
import glob
import os
import sys
import pandas as pd
from rasterio.enums import Resampling
from rasterio import Affine as A
from pyproj import Transformer

"""
Downsample and reproject velocity and thickness data.
"""

base_dir = '/home/jake/usgs/extracted_data/millan_2022'
out_dir = 'data/step1'
res = 100.

tiles = {
    '1.1' : '0',
    '1.2' : '1',
    '1.3' : '2',
    '1.4' : '3',
    '1.5' : '4',
    '1.6' : '5',
    '2.1' : '6',
    '2.2' : '7',
    '2.3' : '8',
    '2.4' : '9'
}




def reproject_field(field, out_name, nodata=np.nan, f=None, transform = None):
    print(field)
    file_names = glob.glob(f'{base_dir}/{field}_*.tif')
    d = {}
    
    for file_name in file_names:
        print(file_name)

        data = rioxarray.open_rasterio(file_name)
        file_name = file_name.split('/')[-1]
        data_name = file_name.split('_')[0]
        tile_name = tiles[file_name.split('_')[1].split('-')[1]]

       
        #nx = int(np.ceil(dx / res))
        #ny = int(np.ceil(dy / res))

        if transform == None:
            src_crs = int(str(data.rio.crs).split(':')[-1])
            dst_crs = 32608
            transformer = Transformer.from_crs(src_crs, dst_crs)
            xx, yy = np.meshgrid(data.x, data.y)
            xs, ys = transformer.transform(xx.flatten(), yy.flatten())
            xmax = xs.max()
            xmin = xs.min()
            ymax = ys.max()
            ymin = ys.min()
            dx = xmax - xmin
            dy = ymax - ymin
            nx = int(np.ceil(dx / res))
            ny = int(np.ceil(dy / res))
        
            dst_transform = A.translation(xmin, ymax) * A.scale(res, -res)
        else:
            nx = transform[tile_name]['nx']
            ny = transform[tile_name]['ny']
            dst_transform = transform[tile_name]['transform']

            
        if f:
            data = f(data)

        #plt.imshow(data[0])
        #plt.colorbar()
        #plt.show()
   
        data = data.rio.reproject(
            'EPSG:32608',
            shape=(ny, nx),
            transform=dst_transform,
            resampling=Resampling.bilinear,
            nodata=nodata,
        )
    
       

        d[tile_name] = {'nx' : nx, 'ny' : ny, 'transform' : dst_transform} 

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)


        raster_name = f'{out_dir}/{out_name}_{tile_name}.tif'
        compress_options = {'compress': 'lzw'} 
        data.rio.to_raster(raster_name, profile=compress_options)

    return d


def replace_nan(data):
    data.data[np.isnan(data.data)] = 0.
    return data

d = reproject_field('V', 'V', f=replace_nan)
reproject_field('STDX', 'VX_STD', transform=d)
reproject_field('STDY', 'VY_STD', transform=d)
reproject_field('VX', 'VX', transform=d)
reproject_field('VY', 'VY', transform=d)
reproject_field('THICKNESS', 'H', transform=d)
reproject_field('ERRTHICKNESS', 'H_ERR', transform=d)
