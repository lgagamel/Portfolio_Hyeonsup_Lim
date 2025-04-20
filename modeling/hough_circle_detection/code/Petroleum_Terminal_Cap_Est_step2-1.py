# =============================================================================
# 
# =============================================================================

import geopandas as gpd
import os
import sys
import numpy as np
import fiona
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
#p1_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity\p1.shp'
p1_capacity_final_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity\p1_capacity_final\p1_capacity_final.shp'

# Read files
with fiona.Env():
    tmp_for_crs = fiona.open(p1_capacity_final_fp)
p1_capacity_final = gpd.read_file(p1_capacity_final_fp)
prj_file  = p1_capacity_final_fp.replace(".shp",".prj")
prj = [l.strip() for l in open(prj_file,'r')][0]

#p1_capacity_final = p1_capacity_final.to_crs(prj)
# calibrate based on capacity weight (beta)

os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P2_Voronoi\beta')
p2 = p1_capacity_final.copy()
p2['count'] = 1
for beta in np.array(range(0,21))/10:
    #p2['capacity_w'] = p2['capacity']**beta
    tmp_col = 'est_b_' + str(beta)
    p2[tmp_col] = p2['est_capaci']**beta    
# Save output    
#p2.to_file('p2_capacity_final.shp',driver='ESRI Shapefile')

p2.to_file('p2_capacity_final.shp',driver='ESRI Shapefile',crs_wkt=prj)
#p2.to_file('p2_capacity_final.shp',driver='ESRI Shapefile')




os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P2_Voronoi\beta3')
p2 = p1_capacity_final.copy()
p2['count'] = 1
n=100
for beta in np.array(range(0,21))/n:
    #p2['capacity_w'] = p2['capacity']**beta
    tmp_col = 'est_b_' + str(int(beta*n))
    p2[tmp_col] = p2['est_capaci']**beta    
# Save output    
#p2.to_file('p2_capacity_final.shp',driver='ESRI Shapefile')

p2.to_file('p2_capacity_final2.shp',driver='ESRI Shapefile',crs_wkt=prj)
#p2.to_file('p2_capacity_final.shp',driver='ESRI Shapefile')

