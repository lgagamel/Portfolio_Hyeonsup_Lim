
import pandas as pd
import numpy as np
import os


ec = pd.read_csv('output/step_1/ec_county.csv',dtype={'ANSI_ST_CO':str,'naics':str}) 

# NAICS_in_CFS = ['212', '311', '312', '313', '314', '315', '316',
#        '321', '322', '323', '324', '325', '326', '327', '331', '332',
#        '333', '334', '335', '336', '337', '339', '423','424','454','493', '511', '551']

NAICS_in_CFS = ['212', '311', '312', '313', '314', '315', '316',
       '321', '322', '323', '324', '325', '326', '327', '331', '332',
       '333', '334', '335', '336', '337', '339', '4231',
       '4232', '4233', '4234', '4235', '4236', '4237', '4238', '4239',
       '4241', '4242', '4243', '4244', '4245', '4246', '4247',
       '4248', '4249', '4541', '45431', '4931', '5111', '551114']




# =============================================================================
# select only 2digit-5digit naics
# =============================================================================
ec = ec.loc[ec['naics'].isin(NAICS_in_CFS)]
#ec = ec.loc[ec['naics'].apply(lambda x: x not in ['31-33','44-45','48-49','45210009(053)'])]
ec['naics'] = ec['naics'].astype(int)
#ec = ec.loc[ec['naics']>=100]
#ec = ec.loc[ec['naics']<1000]

# =============================================================================
# filter out null emp nacis
# =============================================================================
#null_emp_naics = list(ec.loc[np.isnan(ec['emp'])]['naics'].unique())
#ec = ec.loc[ec['naics'].apply(lambda x: x not in null_emp_naics)]


# =============================================================================
# filter out too many null rcptot naics
# =============================================================================
#ec['rcptot_null'] = np.isnan(ec['rcptot'])*1
#ec['cnt'] = 1
#ec_grp = ec.groupby(['naics'],as_index=False)['rcptot_null','cnt'].sum()
#good_naics = list(ec_grp.loc[ec_grp['rcptot_null']<ec_grp['cnt']*0.9]['naics'])
#ec = ec.loc[ec['naics'].apply(lambda x: x in good_naics)]
good_naics = list(set(ec['naics'].unique()))

# =============================================================================
# impute missing for rcptot
# =============================================================================
for tmp_naics in good_naics:
    print(tmp_naics)
    ind = (~np.isnan(ec['rcptot'])) & (ec['naics']==tmp_naics) & (~np.isnan(ec['emp']))
    tmp_ec = ec.loc[ind]
    if (len(tmp_ec)>0) & (sum(tmp_ec['rcptot'])>0) & (sum(tmp_ec['emp'])>0):
        tmp_factor = sum(tmp_ec['rcptot'])/sum(tmp_ec['emp'])
        ind_fix = (np.isnan(ec['rcptot'])) & (ec['naics']==tmp_naics) & (~np.isnan(ec['emp']))
        if tmp_factor>0:
            ec.loc[ind_fix,'rcptot'] = ec.loc[ind_fix,'emp'] * tmp_factor
        else:
            raise('what')





# =============================================================================
# output
# =============================================================================
ec = ec[['ANSI_ST_CO','naics','rcptot']]
ec.to_csv('output/step_2/ec_county.csv', index=False)


ec_pivot = ec.pivot(index='ANSI_ST_CO', columns='naics', values=['rcptot'])
ec_pivot.columns = [str(x[0])+'_'+ str(x[1]) for x in ec_pivot.columns]
ec_pivot = ec_pivot.fillna(0)


# =============================================================================
# drop based on sample size where number>0
# =============================================================================
zero_columns = []
MIN_SAMPLE = 10
for col in ec_pivot.columns:
    if sum(ec_pivot[col]>0)<=MIN_SAMPLE:
        zero_columns = zero_columns + [col]       
ec_pivot = ec_pivot.drop(columns=zero_columns)



# =============================================================================
# Remove naics with identical numbers
# =============================================================================
for col_i in ec_pivot.columns:
    print(col_i)
    for col_j in ec_pivot.columns:
        if (col_i in ec_pivot.columns) & (col_j in ec_pivot.columns) & (col_j != col_i):
            if ec_pivot[col_i].equals(ec_pivot[col_j]):
                ec_pivot = ec_pivot.drop(columns=col_j)
                print('removed',col_j)
                

ec_pivot.to_csv('output/step_2/ec_county_pivot.csv')