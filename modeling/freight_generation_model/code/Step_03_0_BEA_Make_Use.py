import pandas as pd
import numpy as np
import os


# =============================================================================
# Read Data           
# =============================================================================
#cbp_faf = pd.read_csv('output/step_3/cbp_faf_only_3digit_naics.csv')
#cbp_faf = pd.read_csv('output/step_3/cbp_faf.csv')
#cbp_faf_551 = cbp_faf.loc[cbp_faf['naics']==551]
bea_make_use = pd.read_csv('input/BEA_make_use_2012_processed.csv') 



#naics_list = cbp_faf['naics'].unique()


# =============================================================================
# Process bea_make_use
# =============================================================================
col_list = list(bea_make_use.columns)
col_list = col_list[1:]
out = []
for i in range(len(bea_make_use)):
    print(i)
    tmp_line = bea_make_use.iloc[i]
    #tmp_make = tmp_line['Code'][:3]
    tmp_make = tmp_line['Code'][:].replace("0","").replace("A","").replace("B","").replace("C","").replace("D","").replace("E","").replace("F","").replace("G","").replace("H","").replace("I","").replace("J","").replace("K","").replace("L","").replace("M","").replace("N","").replace("O","").replace("P","").replace("Q","").replace("R","").replace("S","").replace("T","").replace("U","").replace("V","").replace("W","").replace("X","").replace("Y","").replace("Z","")
    for col in col_list:
        #tmp_use = col[:3]
        tmp_use = col[:].replace("0","").replace("A","").replace("B","").replace("C","").replace("D","").replace("E","").replace("F","").replace("G","").replace("H","").replace("I","").replace("J","").replace("K","").replace("L","").replace("M","").replace("N","").replace("O","").replace("P","").replace("Q","").replace("R","").replace("S","").replace("T","").replace("U","").replace("V","").replace("W","").replace("X","").replace("Y","").replace("Z","")
        tmp_value = float(str(tmp_line[col]).replace(',',''))
        try:
            tmp_out = [int(tmp_make),int(tmp_use),tmp_value]
            out = out + [tmp_out]
#            if (int(tmp_make) in naics_list) & (int(tmp_use) in naics_list):
#                tmp_out = [int(tmp_make),int(tmp_use),tmp_value]
#                out = out + [tmp_out]
        except:
            pass
        

bea_make_use1 = pd.DataFrame(out,columns=['make','use','value'])


# =============================================================================
# Process bea_make_use
# =============================================================================
col_list = list(bea_make_use.columns)
col_list = col_list[1:]
out = []
for i in range(len(bea_make_use)):
    print(i)
    tmp_line = bea_make_use.iloc[i]
    tmp_make = tmp_line['Code'][:3]
    #tmp_make = tmp_line['Code'][:].replace("0","").replace("A","").replace("B","").replace("C","").replace("D","").replace("E","").replace("F","").replace("G","").replace("H","").replace("I","").replace("J","").replace("K","").replace("L","").replace("M","").replace("N","").replace("O","").replace("P","").replace("Q","").replace("R","").replace("S","").replace("T","").replace("U","").replace("V","").replace("W","").replace("X","").replace("Y","").replace("Z","")
    for col in col_list:
        tmp_use = col[:3]
        #tmp_use = col[:].replace("0","").replace("A","").replace("B","").replace("C","").replace("D","").replace("E","").replace("F","").replace("G","").replace("H","").replace("I","").replace("J","").replace("K","").replace("L","").replace("M","").replace("N","").replace("O","").replace("P","").replace("Q","").replace("R","").replace("S","").replace("T","").replace("U","").replace("V","").replace("W","").replace("X","").replace("Y","").replace("Z","")
        tmp_value = float(str(tmp_line[col]).replace(',',''))
        try:
            tmp_out = [int(tmp_make),int(tmp_use),tmp_value]
            out = out + [tmp_out]
#            if (int(tmp_make) in naics_list) & (int(tmp_use) in naics_list):
#                tmp_out = [int(tmp_make),int(tmp_use),tmp_value]
#                out = out + [tmp_out]
        except:
            pass
        

bea_make_use2 = pd.DataFrame(out,columns=['make','use','value'])

bea_make_use1.to_csv('output/step_3/bea_make_use1.csv',index=False)
bea_make_use2.to_csv('output/step_3/bea_make_use2.csv',index=False)

bea_make_use = bea_make_use1.append(bea_make_use2)
#bea_make_use = pd.DataFrame(out,columns=['use','make','value'])



# =============================================================================
# output directory
# =============================================================================
#os.chdir('output/step_3')

# =============================================================================
# Bea_make_use additional process
# =============================================================================
bea_make_use = bea_make_use.fillna(0)
bea_make_use = bea_make_use.groupby(['make','use'],as_index=False)['value'].sum()
bea_make_use = bea_make_use.loc[bea_make_use['value']>0]
bea_make_use_grp = bea_make_use.groupby(['make'],as_index=False)['value'].sum()
bea_make_use_grp.columns = ['make', 'value_grp']
bea_make_use = bea_make_use.merge(bea_make_use_grp,on='make',how='left')
bea_make_use['ratio'] = bea_make_use['value']/bea_make_use['value_grp'] 
bea_make_use.to_csv('output/step_3/bea_make_use_summary.csv',index=False)


