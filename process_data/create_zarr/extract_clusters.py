import numpy as np
import rioxarray
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import zarr
from datatree import DataTree, open_datatree
import geopandas as gp

glacier_index = 0
datasets = {}

rgi_data = gp.read_file('/media/storage/usgs_data/extracted_data/RGIv6/rgi.shp')
base_dir = '/media/storage/usgs_data/final_data'

def extract_clusters(tile_index, cluster_raster, clusters):

    rasters = {}
    rasters['index'] = cluster_raster
    
    rasters['dem'] = rioxarray.open_rasterio(
        f'{base_dir}/copernicus/DEM_{tile_index}.tif'
    )
    
    rasters['H_millan'] = rioxarray.open_rasterio(
        f'{base_dir}/millan_2022/H_{tile_index}.tif'
    )

    rasters['H_millan_err'] = rioxarray.open_rasterio(
        f'{base_dir}/millan_2022/H_ERR_{tile_index}.tif'
    )

    try:
        rasters['V_millan'] = rioxarray.open_rasterio(
            f'{base_dir}/millan_2022/V_{tile_index}.tif'
        )

        rasters['vx_millan'] = rioxarray.open_rasterio(
            f'{base_dir}/millan_2022/VX_{tile_index}.tif'
        )

        rasters['vy_millan'] = rioxarray.open_rasterio(
            f'{base_dir}/millan_2022/VY_{tile_index}.tif'
        )
    except:
        print('No Millan velocity.')

    spans = ['2000-2005', '2005-2010', '2010-2015', '2015-2020', '2000-2020']

    for span in spans:
        rasters[f'dhdt_{span}'] = rioxarray.open_rasterio(
            f'{base_dir}/hugonnet_2021/dhdt_{span}_{tile_index}.tif'
        )

        rasters[f'dhdt_err_{span}'] = rioxarray.open_rasterio(
            f'{base_dir}/hugonnet_2021/dhdt_err_{span}_{tile_index}.tif'
        )


    try:
        """
        years = range(1985,2019)
        for year in years:
            rasters[f'V_{year}'] = rioxarray.open_rasterio(
                f'{base_dir}/ITS_LIVE/v_{year}_{tile_index}.tif'
            )

            rasters[f'V_err_{year}'] = rioxarray.open_rasterio(
            f'{base_dir}/ITS_LIVE/v_err_{year}_{tile_index}.tif'
            )
        """

        rasters[f'V_2000-2019'] = rioxarray.open_rasterio(
                f'{base_dir}/ITS_LIVE/V_2000-2019_{tile_index}.tif'
        )

        rasters[f'V_err_2000-2019'] = rioxarray.open_rasterio(
            f'{base_dir}/ITS_LIVE/V_err_2000-2019_{tile_index}.tif'
        )
    except:
        print('No ITS LIVE velocity data')
 

    j = 0
    for cluster in clusters:
        print('cluster', cluster)

        indexes = np.argwhere(cluster_raster.data == cluster)

        xi = indexes[:,1]
        yi = indexes[:,2]

        xmin = xi.min() - 5
        xmax = xi.max() + 5
        ymin = yi.min() - 5
        ymax = yi.max() + 5
        xmin = max(0, xmin)
        xmax = min(xmax, rasters['H_millan'].y.size)
        ymin = max(0, ymin)
        ymax = min(ymax, rasters['H_millan'].x.size)

        ds = xr.Dataset()
       
        mask = cluster_raster[0][xmin:xmax, ymin:ymax].copy(deep = True)
        mask.data[mask.data == cluster] = 1
        mask.data[~(mask.data == 1)] = 0
        
        ds.coords['x'] = mask.x.data
        ds.coords['y'] = mask.y.data
        ds['mask'] = (['y', 'x'], mask.data.astype(np.float32))

        for k in rasters:            
            R = rasters[k][0][xmin:xmax, ymin:ymax].copy(deep=True)
            ds[k] = (['y', 'x'], R.data.astype(np.float32))
            #print(k)
            #plt.imshow(ds[k].data)
            #plt.colorbar()
            #plt.show()


        global datasets
        global glacier_index

        rgi_id = str(rgi_data.iloc[cluster-1]['RGIId'])
        print(rgi_id)
        datasets[rgi_id] = ds
        glacier_index += 1
        j += 1


for i in range(10):
    try:
        cluster_raster = rioxarray.open_rasterio(
            f'{base_dir}/RGIv6/RGI_{i}.tif'
        )

        clusters, counts = np.unique(cluster_raster.data[0], return_counts=True)

        clusters = clusters[1:]
        counts = counts[1:]

        areas = counts * 100.*100./1e6
        indexes = areas > 1.
        clusters = clusters[indexes]
        extract_clusters(i, cluster_raster, clusters)
    except Exception as e:
        print(e)

store = zarr.DirectoryStore('glaciers.zarr')
dt = DataTree.from_dict(datasets)
dt.to_zarr(store, mode='w')
