import pandas as pd
import numpy as np


def col_by_naics(df, naics_):
    output_col_list = []
    for col in df.columns:
        # if naics_ in col:
        # print(col)
        if (len(col.split("_"))==2) and (naics_ == col.split("_")[1]):
            output_col_list = output_col_list + [col]
    return output_col_list

XY_cfs_o = pd.read_csv('output/step_6/XY_cfs_o.csv')


naics_list = list(XY_cfs_o['naics'].unique())
df_out = pd.DataFrame()

for naics_ in naics_list:
    # select dataset by naics
    df_naics = XY_cfs_o.loc[XY_cfs_o['naics']==naics_]
    N = len(df_naics)
    
    # obtain a set of variable combinations
    naics_col_list = col_by_naics(df_naics, str(naics_))
    print(naics_,  N, naics_col_list)
    
    df = df_naics[naics_col_list]
    df.columns = [x.replace("_"+str(naics_),"") for x in df.columns]
    
    if ('rcptot' not in df.columns):
        df['rcptot'] = '-'
    
    df = df.describe()
    
    for target_measure in ['tons','value']:
        # df_naics_ = df_naics.loc[df_naics[target_measure+'_f']!='S']
        df_naics_ = df_naics.loc[df_naics[target_measure]>0]
        df[target_measure] = df_naics_.describe()[target_measure] 
        
    df['naics'] = str(naics_)
    df = df.reset_index().rename(columns={'index':'stat'})
    
    df_out = df_out.append(df)
df_out.to_csv('output/step_8/0_Input_Data_Summary/input_data_summary.csv',index=False)