# =============================================================================
# Petroleum_Terminal_Cap_Est_step0-1
# Integrate points where it's close to nearby points
# =============================================================================

import geopandas as gpd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
#p1_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity\p1.shp'
p0_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Reference\20161122_EIA_Petroleum\Data\PetroleumProduct_Terminals_US_EIA\PetroleumProduct_Terminals_US_Aug2015.shp'
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data')
#outfp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0.shp'
# Read files
p0 = gpd.read_file(p0_fp)

prj_file  = p0_fp.replace(".shp",".prj")
prj = [l.strip() for l in open(prj_file,'r')][0]

# create copy of p0
p0_copy1 = p0.copy()
p0_copy2 = p0.copy()

p0_copy1_buffer = p0_copy1.geometry.buffer(0.1)
p0_copy1_buffer = gpd.GeoDataFrame(geometry=p0_copy1_buffer)
p0_intersect = gpd.sjoin(p0_copy1,p0_copy1_buffer,op='within')

output_gpd = gpd.GeoDataFrame()
included = []
for tmp_index in p0_intersect.index.unique():
    if not(tmp_index in included):
        tmp_gpd = p0_intersect.loc[p0_intersect.index_right==tmp_index]
        tmp_gpd_out = tmp_gpd.copy()
        tmp_gpd_out = tmp_gpd_out.iloc[[0]]
        tmp_gpd_out.geometry= tmp_gpd.centroid.iloc[[0]]
        included = included + list(tmp_gpd.index)
        print(list(tmp_gpd.index))
        output_gpd = output_gpd.append(tmp_gpd_out)
        
output_gpd['p0_index'] = np.array(range(len(output_gpd)))
output_gpd.to_file('p0',driver='ESRI Shapefile',crs_wkt=prj)
    