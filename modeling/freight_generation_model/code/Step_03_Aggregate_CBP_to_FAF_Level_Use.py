import pandas as pd
import numpy as np
import os


# =============================================================================
# Read Data           
# =============================================================================
#cbp_faf = pd.read_csv('output/step_3/cbp_faf_only_3digit_naics.csv')
cbp_faf = pd.read_csv('output/step_3/cbp_faf.csv')
cbp_faf_551 = cbp_faf.loc[cbp_faf['naics']==551]
bea_make_use = pd.read_csv('output/step_3/bea_make_use_summary.csv')



naics_list = cbp_faf['naics'].unique()
cbp_faf_out = []
for naics in naics_list:
    #cbp_faf_ = cbp_faf.loc[cbp_faf['naics']==naics]
    naics_ = naics
    bea_make_use_ = bea_make_use.loc[bea_make_use['make']==naics_]
    
    if (len(bea_make_use_)==0):
        naics_ = int(str(naics)[:3])
        bea_make_use_ = bea_make_use.loc[bea_make_use['make']==naics_]
    
    if (len(bea_make_use_)==0):
        naics_ = int(str(naics)[:2])
        bea_make_use_ = bea_make_use.loc[bea_make_use['make']==naics_]
    
    print(naics_,len(bea_make_use_))
    
    #bea_make_use_.to_csv('output/step_3/naics/bea_make_use_'+str(naics)+'.csv')
    
    
    cbp_faf_ = cbp_faf.copy()
    cbp_faf_['naics_'] = cbp_faf_['naics']
    
    use_list = bea_make_use_['use'].unique()
    
    for use_ in use_list:
        cbp_faf_check = cbp_faf_.loc[cbp_faf_['naics_']==use_]
        #print(use_,len(cbp_faf_check))
        
        if (len(cbp_faf_check)==0):
            ind = cbp_faf_['naics_'].apply(lambda x: int(str(x)[:3])==use_)
            cbp_faf_.loc[ind, 'naics_'] = cbp_faf_.loc[ind, 'naics_'].apply(lambda x: int(str(x)[:3]))
            cbp_faf_check = cbp_faf_.loc[cbp_faf_['naics_']==use_]
        
        if (len(cbp_faf_check)==0):
            ind = cbp_faf_['naics_'].apply(lambda x: int(str(x)[:2])==use_)
            cbp_faf_.loc[ind, 'naics_'] = cbp_faf_.loc[ind, 'naics_'].apply(lambda x: int(str(x)[:2]))
            cbp_faf_check = cbp_faf_.loc[cbp_faf_['naics_']==use_]
    
    
    cbp_faf_ = cbp_faf_.merge(bea_make_use_, left_on='naics_',right_on='use',how='right')
    cbp_faf_ = cbp_faf_.loc[cbp_faf_['ratio']>0]
    #cbp_faf_.to_csv('output/step_3/naics/cbp_faf_'+str(naics)+'.csv')
    for col in ['emp','qp1','ap','est','rcptot']:
        cbp_faf_[col] = cbp_faf_[col] * cbp_faf_['ratio']

    cbp_faf_ = cbp_faf_.groupby(['FAF'],as_index=False)['emp', 'qp1', 'ap', 'est','rcptot'].sum()
    cbp_faf_['naics'] = naics
    cbp_faf_ = cbp_faf_[['FAF','naics','emp', 'qp1', 'ap', 'est','rcptot']]
    
    if len(cbp_faf_)>0:
        if len(cbp_faf_out)==0:
            cbp_faf_out = cbp_faf_.copy()
        else:
            cbp_faf_out = cbp_faf_out.append(cbp_faf_)
            
cbp_faf_out = cbp_faf_out.append(cbp_faf_551)

    

# =============================================================================
# Only 3 digit naics
# =============================================================================
cbp_faf_out = cbp_faf_out.groupby(['FAF','naics'],as_index=False)['emp','qp1','ap','est','rcptot'].sum()
cbp_faf_out.to_csv('output/step_3/cbp_faf_use.csv', index=False)

cbp_faf_pivot = cbp_faf_out.pivot(index='FAF', columns='naics', values=['emp','ap','est','rcptot'])
cbp_faf_pivot.columns = [str(x[0])+'_'+ str(x[1]) for x in cbp_faf_pivot.columns]
cbp_faf_pivot = cbp_faf_pivot.fillna(0)
cbp_faf_pivot.to_csv('output/step_3/cbp_faf_pivot_use.csv')