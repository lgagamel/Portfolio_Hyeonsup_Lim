# =============================================================================
# Petroleum_Terminal_Cap_Est_step1-2
# Merge Capacity Estimate from Step 1-1
# =============================================================================


import geopandas as gpd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity')

# File paths
p0_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0\p0.shp'
p0_capacity_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0_capacity\p0_capacity.shp'
p1_out_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity\p1_out.csv'

# Read files
p0 = gpd.read_file(p0_fp)
p0_capacity = gpd.read_file(p0_capacity_fp)
p1_out = pd.read_csv(p1_out_fp)


# get Final estimate and merge into p0_capacity
p0_capacity['est_capacity_final']=p1_out['est_capacity_final']

# fillna and adjust minimum
p0_capacity['est_capacity_final'] = p0_capacity['est_capacity_final'].fillna(0)
p0_capacity['est_capacity_final'] = (p0_capacity['est_capacity_final']==0)*700 +(p0_capacity['est_capacity_final']!=0)*p0_capacity['est_capacity_final']

# group by p0_index
p0_capacity_group = p0_capacity.groupby('p0_index')['est_capacity_final'].sum()

# merge
p1_capacity_final = p0.merge(p0_capacity_group,on='p0_index')

# output shapefile
prj_file  = p0_fp.replace(".shp",".prj")
prj = [l.strip() for l in open(prj_file,'r')][0]
p1_capacity_final.to_file('p1_capacity_final',driver='ESRI Shapefile',crs_wkt=prj)

