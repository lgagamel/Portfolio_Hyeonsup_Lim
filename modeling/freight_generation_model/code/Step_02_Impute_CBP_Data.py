import pandas as pd
import numpy as np
import os


# =============================================================================
# CBP
# =============================================================================
# read csv
cbp = pd.read_csv('output/step_1/cbp_processed.csv',dtype={'ANSI_ST_CO':str,'naics':str})


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
# select only 2digit-5digit naics
# =============================================================================
#ec = ec.loc[ec['naics'].apply(lambda x: x not in ['31-33','44-45','48-49(104)','45210009(053)'])]
cbp = cbp.loc[cbp['naics'].isin(NAICS_in_CFS)]

cbp['naics'] = cbp['naics'].astype(int)
#cbp = cbp.loc[cbp['naics']>=100]
#cbp = cbp.loc[cbp['naics']<1000]

# =============================================================================
# filter out null emp nacis
# =============================================================================
cbp['emp'] = cbp['emp'].astype(float)
cbp.loc[np.isnan(cbp['emp']),'emp'] = 1


# =============================================================================
# filter out too many null rcptot naics
# =============================================================================
cbp['qp1_null'] = np.isnan(cbp['qp1'])*1
cbp['ap_null'] = np.isnan(cbp['ap'])*1
cbp['est_null'] = np.isnan(cbp['est'])*1
cbp['cnt'] = 1

#cbp_grp = cbp.groupby(['naics'],as_index=False)['qp1_null','cnt'].sum()
#good_naics1 = list(cbp_grp.loc[cbp_grp['qp1_null']<cbp_grp['cnt']*1]['naics'])
#cbp_grp = cbp.groupby(['naics'],as_index=False)['ap_null','cnt'].sum()
#good_naics2 = list(cbp_grp.loc[cbp_grp['ap_null']<cbp_grp['cnt']*1]['naics'])
#cbp_grp = cbp.groupby(['naics'],as_index=False)['est_null','cnt'].sum()
#good_naics3 = list(cbp_grp.loc[cbp_grp['est_null']<cbp_grp['cnt']*1]['naics'])
#good_naics = list(set(good_naics1) & set(good_naics2) & set(good_naics3)) 
#cbp = cbp.loc[cbp['naics'].apply(lambda x: x in good_naics)]
#cbp['naics'].unique()

# no filtering
good_naics = list(set(cbp['naics'].unique()))


# =============================================================================
# impute missing 
# =============================================================================
for tmp_col in ['qp1','ap','est']:
    for tmp_naics in good_naics:
        ind = ~np.isnan(cbp[tmp_col]) & (cbp['naics']==tmp_naics) & (cbp['emp']>=0)
        tmp_cbp = cbp.loc[ind]
        if len(tmp_cbp)>0:
            tmp_factor = sum(tmp_cbp[tmp_col])/sum(tmp_cbp['emp'])
            if tmp_factor>0:
                ind_fix = np.isnan(cbp[tmp_col]) & (cbp['naics']==tmp_naics) & (cbp['emp']>=0)
                cbp.loc[ind_fix,tmp_col]= cbp.loc[ind_fix,'emp'] * tmp_factor



# =============================================================================
# wrtie csv file
# =============================================================================
cbp = cbp[['ANSI_ST_CO','naics','emp','qp1','ap','est']]
cbp.to_csv('output/step_2/cbp_county.csv', index=False)

cbp_pivot = cbp.pivot(index='ANSI_ST_CO', columns='naics', values=['emp','ap','est'])
cbp_pivot.columns = [str(x[0])+'_'+ str(x[1]) for x in cbp_pivot.columns]
cbp_pivot = cbp_pivot.fillna(0)

# =============================================================================
# drop based on sample size where number>0
# =============================================================================
zero_columns = []
MIN_SAMPLE = 10
for col in cbp_pivot.columns:
    if sum(cbp_pivot[col]>0)<=MIN_SAMPLE:
        zero_columns = zero_columns + [col]       
cbp_pivot = cbp_pivot.drop(columns=zero_columns)


# =============================================================================
# Remove naics with identical numbers
# =============================================================================
for col_i in cbp_pivot.columns:
    print(col_i)
    for col_j in cbp_pivot.columns:
        if (col_i in cbp_pivot.columns) & (col_j in cbp_pivot.columns) & (col_j != col_i):
            if cbp_pivot[col_i].equals(cbp_pivot[col_j]):
                cbp_pivot = cbp_pivot.drop(columns=col_j)
                print('removed',col_j)
                
cbp_pivot.to_csv('output/step_2/cbp_county_pivot.csv')