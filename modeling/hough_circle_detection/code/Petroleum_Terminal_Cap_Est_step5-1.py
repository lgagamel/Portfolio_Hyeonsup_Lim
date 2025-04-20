import geopandas as gpd
import os
import sys
import pandas as pd
import numpy as np
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P5_State_Level_Validation')
p3_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P3_VMT\p3_out.csv'
p0_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0\p0.shp'
EIA_state_fc_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption\State_EIA_FC.csv'


# Read files
p3 = pd.read_csv(p3_fp)
p0 = gpd.read_file(p0_fp)
EIA_state_fc = pd.read_csv(EIA_state_fc_fp)

# p3 index 
p3 = p3.rename(columns={'FID':'p0_index'})

# final optimum beta
final_beta = 0.18
tmp_p3 = p3.loc[p3.beta==final_beta]

# final shapefile
p5 = p0.copy()
tmp_p4 = p5.merge(tmp_p3,on = 'p0_index', how='left')
tmp_p4_group = tmp_p4.groupby('State')['TFC12','LFC12'].sum()
tmp_p4_group = tmp_p4_group.reset_index(level=tmp_p4_group.index.names)
tmp_p4_group.columns = ['State','TFC12_state','LFC12_state']

# merge tmp_p4_group and EIA_state_fc
p5 = p5.merge(tmp_p3,on = 'p0_index', how='left')
p5 = p5.merge(tmp_p4_group,on = 'State', how='left')
p5 = p5.merge(EIA_state_fc,on = 'State', how='left')

# final estimate
p5['LFC12_final'] = p5['LFC12'] * p5['EIA_LFC12']/p5['LFC12_state']
p5['TFC12_final'] = p5['TFC12'] * p5['EIA_TFC12']/p5['TFC12_state']
p5[['LFC12_final','TFC12_final']] = p5[['LFC12_final','TFC12_final']].fillna(0)

print(sum(p5['LFC12_final']),sum(EIA_state_fc['EIA_LFC12']))
print(sum(p5['TFC12_final']),sum(EIA_state_fc['EIA_TFC12']))
    
# Save output
prj_file  = p0_fp.replace(".shp",".prj")
prj = [l.strip() for l in open(prj_file,'r')][0]
p5.to_file('p5_final',driver='ESRI Shapefile',crs_wkt=prj)

