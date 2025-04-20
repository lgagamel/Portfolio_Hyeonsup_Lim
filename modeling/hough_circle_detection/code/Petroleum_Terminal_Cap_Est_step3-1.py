import geopandas as gpd
import os
import sys
import numpy as np
import pandas as pd
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P3_VMT')
faf_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Reference\20170412_TerminalFuelConsumption\20170412_TerminalFuelConsumption\faf4_esri_arcgis\FAF4.shp'
EIA_state_fc_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption\State_EIA_FC.csv'

# Read files
faf = gpd.read_file(faf_fp)
EIA_state_fc = pd.read_csv(EIA_state_fc_fp)

# control TFC and LFC
control_TFC = sum(EIA_state_fc.EIA_TFC12)
control_LFC = sum(EIA_state_fc.EIA_LFC12)

# faf reorganize
faf = faf[['geometry','VMT12','TVMT12']]
faf['LVMT12'] = faf['VMT12'] - faf['TVMT12']




p3_out = pd.DataFrame(columns=['FID','TVMT12', 'LVMT12','TFC12','LFC12','beta'])
n=100
for beta in np.array(range(0,21))/n:
    tmp_beta = str(int(beta*n))
    p2_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P2_Voronoi\beta3'
    p2_fp = p2_fp + '\\voronoi2_final_b'+tmp_beta + '.shp'
    p2 = gpd.read_file(p2_fp)
    
    # match crs
    #faf = faf.to_crs(p2.crs)
    p2 = p2.to_crs(faf.crs)
    
    # spatial join p2 and faf
    p2_intersect = gpd.sjoin(faf,p2,how='left',op='intersects')
    sum(p2_intersect.FID.fillna(-1)==-1)
    
    # group by 
    p2_intersect_group = p2_intersect.groupby('FID')['TVMT12', 'LVMT12'].sum()
    p2_intersect_group = p2_intersect_group.reset_index(p2_intersect_group.index.names)
    
    tmp_TFC_factor = control_TFC/sum(p2_intersect_group['TVMT12'])
    tmp_LFC_factor = control_LFC/sum(p2_intersect_group['LVMT12'])
    # calculate LFC12 TFC12
    p2_intersect_group['TFC12'] = p2_intersect_group['TVMT12'] * tmp_TFC_factor
    p2_intersect_group['LFC12'] = p2_intersect_group['LVMT12'] * tmp_LFC_factor
    p2_intersect_group['beta'] = beta
    
    p3_out = p3_out.append(p2_intersect_group)
    
# Save output
p3_out.to_csv('p3_out.csv',index=False)
    
