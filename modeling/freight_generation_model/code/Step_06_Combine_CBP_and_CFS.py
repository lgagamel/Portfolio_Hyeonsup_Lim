import pandas as pd
import os

# =============================================================================
# Read data
# =============================================================================
cbp_faf = pd.read_csv('output/step_3/cbp_faf_pivot.csv')
cfs_o = pd.read_csv('output/step_5/cfs_OI.csv')




# =============================================================================
# drop based on sample size where number>0
# =============================================================================
zero_columns = []
MIN_SAMPLE = 10
for col in cbp_faf.columns:
    if sum(cbp_faf[col]>0)<=MIN_SAMPLE:
        zero_columns = zero_columns + [col]       
cbp_faf = cbp_faf.drop(columns=zero_columns)

# =============================================================================
# Remove naics with identical numbers
# =============================================================================
for col_i in cbp_faf.columns:
    print(col_i)
    for col_j in cbp_faf.columns:
        if (col_i in cbp_faf.columns) & (col_j in cbp_faf.columns) & (col_j != col_i):
            if cbp_faf[col_i].equals(cbp_faf[col_j]):
                cbp_faf = cbp_faf.drop(columns=col_j)
                print('removed',col_j)

# =============================================================================
# Column names
# =============================================================================
#cfs_o.columns = ['FAF', 'naics', 'tons', 'value']

# =============================================================================
# Groupby
# =============================================================================
#cfs_o = cfs_o.groupby(['FAF', 'naics'],as_index=False)['tons', 'value'].sum()


# =============================================================================
# Merge
# =============================================================================
XY_cfs_o = cfs_o.merge(cbp_faf,on='FAF',how='left')


# =============================================================================
# Output folder
# =============================================================================
#os.chdir('output/step_6')

XY_cfs_o.to_csv('output/step_6/XY_cfs_o.csv',index=False)