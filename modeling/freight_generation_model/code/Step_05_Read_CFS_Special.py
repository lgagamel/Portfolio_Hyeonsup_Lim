# =============================================================================
# To clean up and reorganize CFS Special Table
# =============================================================================

import pandas as pd
import numpy as np

# =============================================================================
# Input/Output file/folder setting
# =============================================================================
# CFS input csv
infile_path = r'C:\Users\9hl\Dropbox\ORNL\21.Data\03.CFS\2017 CFS special tables\prf_2017_faf03_cfs.txt'


# =============================================================================
# CFS Special Tables - Table 1 ODCM
# =============================================================================
# read csv
cfs_0 = pd.read_csv(infile_path, sep='|')
#cfs_0 = cfs_0.loc[cfs_0['origin']=='0100000US']
#cfs_0 = cfs_0.loc[cfs_0['destination']=='0100000US']
#cfs_0 = cfs_0.loc[cfs_0['fafmode']==1]
#cfs_0.to_csv('output/step_5/cfs_raw.csv', index=False)

# =============================================================================
# # column list
# origin – The origin geography code.
# origin_description  – The description of the origin geography.
# destination – The destination geography code.
# destination_description – The description of the destination geography.
# fafmode – The FAF mode code.
# fafmode_description – The description of the FAF mode.
# naics – The naics code 
# naics_description – The description of the naics code.
# value_in_millions – The shipment value in millions.
# value_cv – The reliability estimate for Value. 
# tons_in_thousands The shipment weight in tons.
# tons_cv – The reliability estimate for Tons.
# unwghtshpcnt – The unweighted shipment count rounded to the nearest 5 (e.g.  1->5, 9->5, 322->325, etc.).# 
# =============================================================================

# CFS zone to FAF zone
#cfs_to_faf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\10.GIS\CFS\CFS_FAF_Zone.csv')
cfs_to_faf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\10.GIS\CFS\CFS_FAF_Zone2017.csv')
cfs_to_faf = cfs_to_faf[['CFS12GEOID','FAF']]
cfs_to_faf = cfs_to_faf.append([pd.DataFrame([['0100000US',0]],columns=cfs_to_faf.columns)])
cfs_to_faf_o = cfs_to_faf.copy()
cfs_to_faf_d = cfs_to_faf.copy()
cfs_to_faf_o.columns = ['origin','O']
cfs_to_faf_d.columns = ['destination','D']
cfs_0 = cfs_0.merge(cfs_to_faf_o, on = 'origin', how='left')
cfs_0 = cfs_0.merge(cfs_to_faf_d, on = 'destination', how='left')

# filter out other levels of geography (132 faf zones + all (0))
cfs_0 = cfs_0.loc[~np.isnan(cfs_0.O)]
cfs_0 = cfs_0.loc[~np.isnan(cfs_0.D)]

# Change Var names
cfs_0 = cfs_0.rename(
        columns={'tons_in_thousands':'tons',
                 'value_in_millions':'value',                 
                 'naics':'I',
                 'fafmode':'M',
                 'unwghtshpcnt':'cnt'})
    
# selective columns
cfs_0 = cfs_0[['O','D','I','M','tons','value','tons_cv','value_cv','cnt']]


#cfs_0 = cfs_0.loc[cfs_0['I']!='31-33']
cfs_0 = cfs_0.loc[cfs_0['I'].isin(['00', '212', '311', '312', '313', '314', '315', '316',
       '321', '322', '323', '324', '325', '326', '327', '331', '332',
       '333', '334', '335', '336', '337', '339', '423','424','4541', '45431', '4931', '5111', '551114'])]

len(['212', '311', '312', '313', '314', '315', '316',
       '321', '322', '323', '324', '325', '326', '327', '331', '332',
       '333', '334', '335', '336', '337', '339', '423','424','454','493','511','551'])

print('previous',cfs_0['I'].unique())
# cfs_0['I'] = cfs_0['I'].apply(lambda x: x[:3])
cfs_0['I'] = np.array(cfs_0['I'].astype(int))
print('after',cfs_0['I'].unique())

cfs_0['O'] = np.array(cfs_0['O'].astype(int))
cfs_0['D'] = np.array(cfs_0['D'].astype(int))


# change mode (0: all modes)
cfs_0['M'] = np.array(cfs_0['M'].replace({1:0}))

# add columns to indicate suppressed
cfs_0['tons_s'] = np.array((cfs_0['tons']=='S')*1)
cfs_0['value_s'] = np.array((cfs_0['value']=='S')*1)

# changed suppressed cells to NaN
cfs_0['tons'] = np.array(pd.to_numeric(cfs_0['tons'], errors='coerce'))
cfs_0['value'] = np.array(pd.to_numeric(cfs_0['value'], errors='coerce'))
cfs_0['tons_cv'] = np.array(pd.to_numeric(cfs_0['tons_cv'], errors='coerce'))
cfs_0['value_cv'] = np.array(pd.to_numeric(cfs_0['value_cv'], errors='coerce'))

# filter full ODCM matrix and marginal total (higher dimension)
ind_full = (cfs_0.O>0)&(cfs_0.D>0)&(cfs_0.I>0)&(cfs_0.M>0)
ind_oi = (cfs_0.O>0)&(cfs_0.D==0)&(cfs_0.I>0)&(cfs_0.M==0)
ind_di = (cfs_0.O==0)&(cfs_0.D>0)&(cfs_0.I>0)&(cfs_0.M==0)
cfs_0_full = cfs_0.loc[ind_full]
cfs_0_margin = cfs_0.loc[~ind_full]
cfs_0_oi = cfs_0.loc[ind_oi]
cfs_0_di = cfs_0.loc[ind_di]
# save output
#cfs_0.to_csv('output/step_5/cfs_ODIM_all.csv', index=False)
# cfs_0_full.to_csv('output/step_5/cfs_ODIM_full.csv', index=False)
#cfs_0_margin.to_csv('output/step_5/cfs_ODIM_margin.csv', index=False)
# cfs_0_oi.to_csv('output/step_5/cfs_OI.csv', index=False)
cfs_0_oi = cfs_0_oi.groupby(['O', 'I'],as_index=False)['tons', 'value'].sum()

cfs_0_oi.columns = ['FAF', 'naics', 'tons', 'value']

cfs_0_oi.to_csv('output/step_5/cfs_OI.csv', index=False)