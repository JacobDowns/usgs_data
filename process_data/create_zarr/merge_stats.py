import numpy as np
import pandas as pd
import geopandas as gp

rgi_data = gp.read_file('/media/storage/usgs_data/extracted_data/RGIv6/rgi.shp')
rgi_data = rgi_data[['RGIId', 'Name', 'CenLon', 'CenLat']]

base_dir = '/media/storage/usgs_data/final_data'

data = pd.read_csv('stats.csv')

data = pd.merge(data, rgi_data, on='RGIId', how='inner')
data['Name'].fillna('None', inplace=True)
data.to_csv('stats_data.csv')