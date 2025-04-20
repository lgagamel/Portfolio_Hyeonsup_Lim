import pandas as pd
import os
import numpy as np

# =============================================================================
# output directory
# =============================================================================
#os.chdir('output/step_4')


# =============================================================================
# CFS PUM
# =============================================================================
cfs_pum = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\03.CFS\2017_CFS_PUM\cfs-2017-puf-csv\CSV.csv')
cfs_pum = cfs_pum[['SCTG','NAICS','SHIPMT_WGHT','SHIPMT_VALUE','WGT_FACTOR']]
cfs_pum['value']=cfs_pum['SHIPMT_VALUE']*cfs_pum['WGT_FACTOR']/1000000 # dollar to million dollars
cfs_pum['tons']=cfs_pum['SHIPMT_WGHT']*cfs_pum['WGT_FACTOR']/2000000 # pounds to thousand short-tons
cfs_pum = cfs_pum[['SCTG','NAICS','tons','value']]    
cfs_pum.columns = ['C','I','tons','value']
cfs_pum['cnt']=1
cfs_pum['C'] = cfs_pum['C'].replace({'01-05':'00','06-09':'00','10-14':'00','15-19':'00','20-24':'00','25-30':'00','31-34':'00','35-38':'00','39-43':'00'})
cfs_pum['C'] = cfs_pum['C'].astype(int)
cfs_pum = cfs_pum.loc[cfs_pum['C']>0]


# =============================================================================
# naics in CFS
# =============================================================================
NAICS_in_CFS = ['212', '311', '312', '313', '314', '315', '316',
       '321', '322', '323', '324', '325', '326', '327', '331', '332',
       '333', '334', '335', '336', '337', '339', '4231',
       '4232', '4233', '4234', '4235', '4236', '4237', '4238', '4239',
       '4241', '4242', '4243', '4244', '4245', '4246', '4247',
       '4248', '4249', '4541', '45431', '4931', '5111', '551114']


# =============================================================================
# filter for NAICS
# =============================================================================
cfs_pum = cfs_pum.loc[cfs_pum['I'].isin(NAICS_in_CFS)]



# =============================================================================
# CFS PUM reformat NAICS code
# =============================================================================
#cfs_pum['I'] = cfs_pum['I'].astype(str)
#cfs_pum['I'] = cfs_pum['I'].apply(lambda x: x[:3])
cfs_pum['I'] = cfs_pum['I'].astype(int)


# =============================================================================
# by CI
# =============================================================================
cfs_pum_grp = cfs_pum.groupby(['C','I'],as_index=False)['cnt','tons','value'].sum()
cfs_pum_grp_by_C = cfs_pum.groupby(['C'],as_index=False)['tons','value'].sum()
cfs_pum_grp_by_C.columns = ['C','tons_by_C','value_by_C']
cfs_pum_grp = cfs_pum_grp.merge(cfs_pum_grp_by_C, on = ['C'], how='left')
cfs_pum_grp['tons_p'] = cfs_pum_grp['tons'] / cfs_pum_grp['tons_by_C'] 
cfs_pum_grp['value_p'] = cfs_pum_grp['value'] / cfs_pum_grp['value_by_C'] 
cfs_pum_grp.to_csv('output/step_4/cfs_pum_2017_by_CI.csv', index=False)

