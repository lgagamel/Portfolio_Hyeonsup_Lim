import pandas as pd
import numpy as np
import os


# =============================================================================
# Read Data           
# =============================================================================
cbp = pd.read_csv('output/step_2/cbp_county.csv') 
ec = pd.read_csv('output/step_2/ec_county.csv') 
county_to_faf = pd.read_csv('input/cbp_county_to_faf.csv') 

# =============================================================================
# Merge cbp and ec
# =============================================================================
cbp = cbp.merge(ec,on=['ANSI_ST_CO','naics'],how='left')


# =============================================================================
# Merge
# =============================================================================
cbp = cbp.merge(county_to_faf[['ANSI_ST_CO','FAF']],on='ANSI_ST_CO',how='left')
cbp = cbp[['ANSI_ST_CO','FAF','naics','emp','qp1','ap','est','rcptot']]
ind = np.isnan(cbp['FAF'])
cbp.loc[ind].to_csv('cbp_county_no_matching_FAF.csv', index=False)
cbp = cbp.loc[~np.isnan(cbp['FAF'])]


# =============================================================================
# Group by FAF
# =============================================================================
cbp_faf = cbp.groupby(['FAF','naics'],as_index=False)['emp','qp1','ap','est','rcptot'].sum()


# =============================================================================
# Optional - share instead of actual tonnage
# =============================================================================
#cbp_faf_grp = cbp.groupby(['naics'],as_index=False)['emp','qp1','ap','est','rcptot'].sum()
#cbp_faf_grp.columns = ['naics','emp_grp','qp1_grp','ap_grp','est_grp','rcptot_grp']
#
#cbp_faf = cbp_faf.merge(cbp_faf_grp, on =['naics'],how='left')
#
#for col in ['emp','qp1','ap','est','rcptot']:
#    cbp_faf[col] = cbp_faf[col] / cbp_faf[col+'_grp']

cbp_faf = cbp_faf[['FAF','naics','emp','qp1','ap','est','rcptot']]

# =============================================================================
# output directory
# =============================================================================
#


# =============================================================================
# Output
# =============================================================================
cbp_faf.to_csv('output/step_3/cbp_faf.csv', index=False)

cbp_faf_pivot = cbp_faf.pivot(index='FAF', columns='naics', values=['emp','ap','est','rcptot'])
cbp_faf_pivot.columns = [str(x[0])+'_'+ str(x[1]) for x in cbp_faf_pivot.columns]
cbp_faf_pivot = cbp_faf_pivot.fillna(0)
cbp_faf_pivot.to_csv('output/step_3/cbp_faf_pivot.csv')



# =============================================================================
# Only 3 digit naics
# =============================================================================
#cbp_faf = cbp_faf.loc[(cbp_faf['naics']>=100)&(cbp_faf['naics']<1000)]
#cbp_faf.to_csv('output/step_3/cbp_faf_only_3digit_naics.csv', index=False)
#
#cbp_faf_pivot = cbp_faf.pivot(index='FAF', columns='naics', values=['emp','ap','est','rcptot'])
#cbp_faf_pivot.columns = [str(x[0])+'_'+ str(x[1]) for x in cbp_faf_pivot.columns]
#cbp_faf_pivot = cbp_faf_pivot.fillna(0)
#drop_columns = []
#for col in cbp_faf_pivot.columns:
#    if sum(cbp_faf_pivot[col])==0:
#        drop_columns = drop_columns + [col]
#cbp_faf_pivot = cbp_faf_pivot.drop(columns=drop_columns)
#cbp_faf_pivot.to_csv('output/step_3/cbp_faf_pivot_only_3digit_naics.csv')