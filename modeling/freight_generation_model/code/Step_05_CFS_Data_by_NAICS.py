# =============================================================================
# To clean up and reorganize CFS Special Table
# =============================================================================

import pandas as pd
import os
import numpy as np


# =============================================================================
# Input/Output file/folder setting
# =============================================================================
# CFS input csv
#infile_path = r'C:\Users\9hl\Dropbox\ORNL\21.Data\03.CFS\FAF_2017_csv\prf_2017_faf01_cfs.txt'

# change working directory for outputs



# =============================================================================
# CFS Special Tables - Table 1 ODCM
# =============================================================================
# read csv
df = pd.read_csv('input/CF1700A08.dat', sep='|')

df = df.loc[df['YEAR']==2017]

df_ = df.loc[df['GEOTYPE']==1]
df_.groupby(['NAICS2012', 'NAICS2012_TTL'], as_index=False)['TON'].sum().to_csv('output/step_5/CFS_2017_NAICS_all.csv', index=False)


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
df = df.loc[df['NAICS2012'].isin(NAICS_in_CFS)]


# =============================================================================
# save NAICS codes
# =============================================================================
df_ = df.loc[df['GEOTYPE']==1]
df_.groupby(['NAICS2012', 'NAICS2012_TTL'], as_index=False)['TON'].sum().to_csv('output/step_5/CFS_2017_NAICS.csv', index=False)




# =============================================================================
# filter
# =============================================================================
df = df.loc[df['GEOTYPE']==16]



# CFS zone to FAF zone
#cfs_to_faf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\10.GIS\CFS\CFS_FAF_Zone.csv')
cfs_to_faf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\10.GIS\CFS\CFS_FAF_Zone2017.csv')
cfs_to_faf = cfs_to_faf[['CFS12GEOID','FAF']]
#cfs_to_faf = cfs_to_faf.append([pd.DataFrame([['0100000US',0]],columns=cfs_to_faf.columns)])
cfs_to_faf.columns = ['GEO_ID','O']
df = df.merge(cfs_to_faf, on = 'GEO_ID', how='left')


# =============================================================================
# selected columns
# =============================================================================
df = df[['O','NAICS2012','TON','VAL','TON_F','VAL_F']]
df.columns = ['FAF', 'naics', 'tons', 'value','tons_f','value_f']

# =============================================================================
# output
# =============================================================================
df.to_csv('output/step_5/cfs_OI.csv', index=False)
