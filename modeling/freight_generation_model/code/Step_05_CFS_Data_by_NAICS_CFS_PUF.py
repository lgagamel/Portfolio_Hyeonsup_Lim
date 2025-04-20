# =============================================================================
# Library
# =============================================================================
import pandas as pd
import numpy as np


# =============================================================================
# Read Data
# =============================================================================
cfs_puf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\03.CFS\2017_CFS_PUM\cfs-2017-puf-csv\CSV.csv')

print(list(cfs_puf.columns))

# =============================================================================
# Filtering & Processing
# =============================================================================
# filter variables that are used in the modeling. 
cfs_puf = cfs_puf[['ORIG_CFS_AREA','DEST_CFS_AREA','NAICS','SCTG','MODE','SHIPMT_VALUE','SHIPMT_WGHT','SHIPMT_DIST_ROUTED','WGT_FACTOR']]    

# CFS zone to FAF zone
#cfs_to_faf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\10.GIS\CFS\CFS_FAF_Zone.csv')
#cfs_to_faf = cfs_to_faf[['ST_MA12','FAF']]
cfs_to_faf = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\21.Data\10.GIS\CFS\CFS_FAF_Zone2017.csv')
cfs_to_faf = cfs_to_faf[['ST_MA','FAF']]
cfs_to_faf_o = cfs_to_faf.copy()
cfs_to_faf_d = cfs_to_faf.copy()
cfs_to_faf_o.columns = ['ORIG_CFS_AREA','dms_orig']
cfs_to_faf_d.columns = ['DEST_CFS_AREA','dms_dest']
cfs_puf = cfs_puf.merge(cfs_to_faf_o, on = 'ORIG_CFS_AREA', how='left')
cfs_puf = cfs_puf.merge(cfs_to_faf_d, on = 'DEST_CFS_AREA', how='left')

# filter out other levels of geography (132 faf zones + all (0))
cfs_puf = cfs_puf.loc[~np.isnan(cfs_puf.dms_orig)]
# cfs_puf = cfs_puf.loc[~np.isnan(cfs_puf.dms_dest)]

cfs_puf['dms_orig'] = cfs_puf['dms_orig'].fillna(0)
cfs_puf['dms_dest'] = cfs_puf['dms_dest'].fillna(0)
cfs_puf['dms_orig'] = np.array(cfs_puf['dms_orig'].astype(int))
cfs_puf['dms_dest'] = np.array(cfs_puf['dms_dest'].astype(int))



# an estimate of the total value/weight for a given domain
cfs_puf['cfs2017_value']=cfs_puf['SHIPMT_VALUE']*cfs_puf['WGT_FACTOR']/1000000 # dollar to million dollars
cfs_puf['cfs2017_tons']=cfs_puf['SHIPMT_WGHT']*cfs_puf['WGT_FACTOR']/2000000 # pounds to thousand short-tons
cfs_puf['cfs2017_tmiles']=cfs_puf['cfs2017_tons']*cfs_puf['SHIPMT_DIST_ROUTED']/1000


# Change Var names
cfs_puf = cfs_puf.rename(columns={'SCTG':'sctg2','MODE':'dms_mode'})


# C
cfs_puf['sctg2'] = np.array(cfs_puf['sctg2'].replace({'01-05':'00','06-09':'00','10-14':'00','15-19':'00','20-24':'00','25-30':'00','31-34':'00','35-38':'00','39-43':'00'}))
cfs_puf['sctg2'] = np.array(cfs_puf['sctg2'].astype(int))
# cfs_puf = cfs_puf.loc[cfs_puf.C>0]

# change mode (0: all modes)
cfs_puf['dms_mode'] = np.array(cfs_puf['dms_mode'].astype(int))
cfs_puf['dms_mode'] = np.array(cfs_puf['dms_mode'].replace({3:1,4:1,5:1,6:2,7:3,8:3,9:3,10:3,101:3,11:4,12:6,13:5,14:5,15:5,16:5,17:5,18:5,19:7,20:5}))
# cfs_puf = cfs_puf.loc[cfs_puf.M>0]

cfs_puf['dms_orig'] = cfs_puf['dms_orig'].apply(lambda x: str(x).zfill(3))
cfs_puf['dms_dest'] = cfs_puf['dms_dest'].apply(lambda x: str(x).zfill(3))

cfs_puf['sctg2'] = cfs_puf['sctg2'].apply(lambda x: str(x).zfill(2))
cfs_puf['dms_mode'] = cfs_puf['dms_mode'].apply(lambda x: str(x).zfill(1))


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
cfs_puf['NAICS'] = cfs_puf['NAICS'].astype(str)
cfs_puf = cfs_puf.loc[cfs_puf['NAICS'].isin(NAICS_in_CFS)]



# cfs_puf = cfs_puf.groupby(['dms_orig','dms_dest','sctg2','dms_mode'],as_index=False)['cfs2017_tons','cfs2017_value','cfs2017_tmiles'].sum()
cfs_puf = cfs_puf.groupby(['dms_orig','NAICS'],as_index=False)['cfs2017_tons','cfs2017_value'].sum()
cfs_puf.columns = ['FAF', 'naics', 'tons', 'value']
cfs_puf.to_csv('output/step_5/cfs_OI_.csv',index=False)

