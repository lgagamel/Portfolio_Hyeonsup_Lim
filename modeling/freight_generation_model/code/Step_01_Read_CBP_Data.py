import pandas as pd
import numpy as np

# =============================================================================
# CBP
# =============================================================================
# read csv
cbp = pd.read_csv('input/cbp17co.txt')

cbp['fipstate'] = cbp['fipstate'].astype(str).apply(lambda x: x.zfill(2))
cbp['fipscty'] = cbp['fipscty'].astype(str).apply(lambda x: x.zfill(3))
cbp['ANSI_ST_CO'] = cbp['fipstate'] +  cbp['fipscty']

# filter variables that are used in the modeling. 
#cbp = cbp[['ANSI_ST_CO','naics','empflag','emp_nf','emp','qp1_nf','qp1','ap_nf','ap','est']]
cbp = cbp[['ANSI_ST_CO','naics','empflag','emp_nf','emp','qp1_nf','qp1','ap_nf','ap','est','n<5', 'n5_9', 'n10_19', 'n20_49','n50_99', 'n100_249', 'n250_499', 'n500_999', 'n1000', 'n1000_1','n1000_2', 'n1000_3', 'n1000_4']]
cbp.columns = ['ANSI_ST_CO','naics','empflag','emp_nf','emp','qp1_nf','qp1','ap_nf','ap','est','n1_4', 'n5_9', 'n10_19', 'n20_49','n50_99', 'n100_249', 'n250_499', 'n500_999', 'n1000', 'n1000_1','n1000_2', 'n1000_3', 'n1000_4']

# =============================================================================
# data format
# =============================================================================
cbp['naics'] = cbp['naics'].str.replace('/','')
cbp['naics'] = cbp['naics'].str.replace('-','')
cbp['naics'] = cbp['naics'].replace('',0)
cbp['naics'] = cbp['naics'].astype(int)
cbp = cbp.loc[cbp['naics']>0]
cbp = cbp.loc[cbp['naics']<1000000]

# =============================================================================
# null values
# =============================================================================
cbp['empflag'] = cbp['empflag'].replace({'A':9.5,"B":59.5,"C":174.5,"E":374.5,"F":749.5,"G":1749.5, "H":3749.5,"I":7499.5,"J":17499.5,"K":37499.5, "L":74999.5, "M":150000})
#cbp['emp']=np.where((cbp['emp_nf']=='D') | (cbp['emp_nf']=='S'),np.nan,cbp['emp'])
#cbp['emp']=np.where(np.isnan(cbp['emp']),cbp['empflag'] ,cbp['emp'])
cbp['emp']=np.where((cbp['emp_nf']=='S'),cbp['empflag'] ,cbp['emp'])
cbp['emp']= cbp['est'] + cbp['emp'] 
#cbp['emp']=np.where(np.isnan(cbp['emp']),cbp['est'] ,cbp['emp'])
cbp['qp1']=np.where((cbp['qp1_nf']=='D') | (cbp['qp1_nf']=='S'),np.nan,cbp['qp1'])
cbp['ap']=np.where((cbp['ap_nf']=='D') | (cbp['ap_nf']=='S'),np.nan,cbp['ap'])


# =============================================================================
# wrtie csv file
# =============================================================================
cbp.to_csv('output/step_1/cbp_processed.csv', index=False)

