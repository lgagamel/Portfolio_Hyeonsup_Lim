import geopandas as gpd
import os
import sys
import pandas as pd
import numpy as np
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption')
p3_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P3_VMT\p3_out.csv'
p0_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0\p0.shp'
EIA_state_fc_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption\State_EIA_FC.csv'

# Read files
p3 = pd.read_csv(p3_fp)
p0 = gpd.read_file(p0_fp)
EIA_state_fc = pd.read_csv(EIA_state_fc_fp)

# p3 index 
p3 = p3.rename(columns={'FID':'p0_index'})

def r_squared(y_obs, y_est):    
    y_mean = np.mean(y_obs)
    SS_err = np.sum((y_est - y_obs)**2)
    SS_tot = np.sum((y_mean - y_obs)**2)
    return 1 - (SS_err/SS_tot)

p4_summary = pd.DataFrame(columns=['beta','r2_TFC','r2_LFC'])
n=100
for beta in np.array(range(0,21))/n:
    tmp_p3 = p3.loc[p3.beta==beta]
    tmp_p4 = p0.merge(tmp_p3,on = 'p0_index', how='left')
    tmp_p4_group = tmp_p4.groupby('State')['TFC12','LFC12'].sum()
    tmp_p4_group = tmp_p4_group.reset_index(level=tmp_p4_group.index.names)
    
    tmp_test_df = EIA_state_fc.merge(tmp_p4_group, on='State', how='left')
    
    r2_TFC = r_squared(tmp_test_df.EIA_TFC12, tmp_test_df.TFC12)
    r2_LFC = r_squared(tmp_test_df.EIA_LFC12, tmp_test_df.LFC12)
    
    tmp_p4_summary = pd.DataFrame([[beta,r2_TFC,r2_LFC]],columns=['beta','r2_TFC','r2_LFC'])
    p4_summary = p4_summary.append(tmp_p4_summary)
    
# Save output
p4_summary.to_csv('p4_summary.csv')


plt.plot(p4_summary.beta,p4_summary.r2_LFC)
