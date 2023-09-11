import numpy as np
import rioxarray
import xarray as xr
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Extract data for the refined clusters
def smooth(U, sigma=1.5):    
    truncate=4.0     
    V=U.copy()
    V[np.isnan(U)]=0
    VV=gaussian_filter(V,sigma=sigma,truncate=truncate)
    W=0*U.copy()+1
    W[np.isnan(U)]=0
    WW=gaussian_filter(W,sigma=sigma,truncate=truncate)
    Z=VV/WW
    return Z

def get_mean(tile_index):
    base_dir = '/media/storage/usgs_data/final_data'

    index = rioxarray.open_rasterio(
        f'{base_dir}/RGIv6/RGI_{tile_index}.tif'
    )


    h = rioxarray.open_rasterio(
        f'{base_dir}/millan_2022/H_{tile_index}.tif'
    )

    #plt.imshow(h.data[0])
    #plt.show()

    """
    v_dict = {}
    for y in range(2000, 2019):

        v_data = rioxarray.open_rasterio(
            f'{base_dir}/ITS_LIVE/v_{y}_{tile_index}.tif'
        )

        v_err_data = rioxarray.open_rasterio(
            f'{base_dir}/ITS_LIVE/v_err_{y}_{tile_index}.tif'
        )

        v_dict[y] = {
            'v' : v_data.data,
            'v_err' : v_err_data.data
        }
    """
    
    Vs = []
    years = np.arange(2000, 2019)
    j = 0
    for y in years:
        v = rioxarray.open_rasterio(
            f'{base_dir}/ITS_LIVE/v_{y}_{tile_index}.tif'
        )
        
        if j == 0:
            mask = xr.ones_like(v)
            
        mask.data[0][np.isnan(v.data[0])] = 0.
        mask.data[0][v.data[0] <= 0.] = 0.
        Vs.append(v.data[0])


    
    indexes = mask.data[0] == 0.
    for j in range(len(years)):
        Vs[j][indexes] = np.nan
        
    V = np.nanmean(Vs, axis=0)
    V_m = xr.zeros_like(h)
    V_m.data[0] = V
    
      
    V_m.rio.to_raster(f'{base_dir}/ITS_LIVE/V_mean_{tile_index}.tif')
    mask.rio.to_raster(f'{base_dir}/ITS_LIVE/V_mask_{tile_index}.tif')


for i in range(10):
    print(i)
    try:
        get_mean(i)
    except Exception as e:
        print(e)
   

