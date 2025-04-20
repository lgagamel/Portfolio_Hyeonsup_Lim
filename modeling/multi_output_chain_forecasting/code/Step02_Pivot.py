# =============================================================================
# library
# =============================================================================
import pandas as pd
import os

# =============================================================================
# load data
# =============================================================================
dtype={"HS":str,"Year":int,"Month":int,"Value":float,"Quantity":float,"Price":float}

for trade_type in ["Import","Export"]:
    df = pd.read_csv('output/step1/'+trade_type+'.csv',dtype=dtype)
    for measure in ["Value"]:
        df_out = df.pivot(index=["Year", "Month"], columns=["HS"],values=measure)
        df_out = df_out.dropna(axis=1)
        df_out = df_out.reset_index()
        df_out.to_csv('output/step2/'+trade_type+'_'+measure+'.csv',index=False)

