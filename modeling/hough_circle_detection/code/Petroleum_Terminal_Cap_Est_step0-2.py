# =============================================================================
# Petroleum_Terminal_Cap_Est_step0-2
# Merge capacity data into p0 from step0-1
# =============================================================================

import geopandas as gpd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
#p1_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity\p1.shp'
p0_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0\p0.shp'
capacity_fp = r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\1908_Petroleum_Terminal_Cap_Est\Input\TerminalCapacity_ESL.csv'
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data')
#outfp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0_capacity.shp'
#outfp_df = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0_capacity.csv'

# Read files
p0 = gpd.read_file(p0_fp)
capacity = pd.read_csv(capacity_fp)

# Create geopandas
capacity = gpd.GeoDataFrame(capacity, geometry=gpd.points_from_xy(capacity.Longitude, capacity.Latitutde))
capacity.crs = p0.crs

prj_file  = p0_fp.replace(".shp",".prj")
prj = [l.strip() for l in open(prj_file,'r')][0]

# create copy of p0
p0_copy1 = p0.copy()

# create buffer
p0_copy1_buffer = p0_copy1.geometry.buffer(0.1)
p0_copy1_buffer = gpd.GeoDataFrame(p0_copy1[['p0_index']], geometry=p0_copy1_buffer)
p0_intersect = gpd.sjoin(p0_copy1_buffer,capacity,how='left',op='intersects')

p0_intersect['TerminalCapacity (barrels)'] = p0_intersect['TerminalCapacity (barrels)'].fillna(-1)

p0_intersect.Longitude = p0_intersect.Longitude.fillna(-1)
p0_intersect.Latitutde = p0_intersect.Latitutde.fillna(-1)

for i in range(len(p0_intersect)):
    print(i)
    tmp_gpd = p0_intersect.iloc[i]
    if tmp_gpd.Longitude == -1:
        print(i,'--')
        p0_intersect['Longitude'].iloc[i] = tmp_gpd.geometry.centroid.y
        p0_intersect['Latitutde'].iloc[i] = tmp_gpd.geometry.centroid.x

p0_intersect[['TerminalCapacity (barrels)','Longitude','Latitutde']]

p0_intersect.to_file('p0_capacity',driver='ESRI Shapefile',crs_wkt=prj)
p0_intersect_df = pd.DataFrame(p0_intersect)
p0_intersect_df = p0_intersect_df.drop('geometry',axis=1)
p0_intersect_df.to_csv('p0_capacity.csv',index=False)
    