# =============================================================================
# library
# =============================================================================
import pandas as pd
import os
from datetime import datetime

# =============================================================================
# load data
# =============================================================================
dtype={"HS":str,"Year":int,"Month":int,"Value":float,"Quantity":float,"Price":float}


i = 0 
for trade_type in ["Import","Export"]:    
    for measure in ["Value"]:
        df = pd.read_csv('output/step2/'+trade_type+'_'+measure+'.csv',dtype=dtype)
        df.columns = [trade_type+"_"+measure+"_"+x if x not in ["Year","Month"] else x for x in df.columns]        
        if i == 0:
            df_out = df.copy()
        else:
            df_out = df_out.merge(df,on=["Year","Month"],how="left")
        i = i + 1



# =============================================================================
# index time
# =============================================================================
df_out["Time"] = df_out.apply(lambda x: datetime(int(x["Year"]), int(x["Month"]),1),axis=1)

# https://www.aptean.com/en-US/insights/blog/6-events-disrupted-maunfacturing-supply-chain
# =============================================================================
# variable to indicate invasion
# =============================================================================
df_out["Invasion"] = 0
ind = (df_out["Time"]>="2022-02-01")
df_out.loc[ind,"Invasion"] = 1

# =============================================================================
# variable to indicate covid & Brexit
# =============================================================================
df_out["Covid"] = 0
ind = (df_out["Time"]>="2020-01-01")
df_out.loc[ind,"Covid"] = 1

# =============================================================================
# variable to indicate suez canal
# =============================================================================
df_out["Suez"] = 0
ind = (df_out["Time"]=="2021-03-01")
df_out.loc[ind,"Suez"] = 1

# =============================================================================
# Big freeze in USA
# =============================================================================
df_out["Freeze"] = 0
ind = (df_out["Time"]=="2021-02-01")
df_out.loc[ind,"Freeze"] = 1

# =============================================================================
# variable to indicate Great Recession
# =============================================================================
df_out["Recession"] = 0
ind = (df_out["Time"]>="2007-12-01")&(df_out["Time"]<="2009-06-01")
df_out.loc[ind,"Recession"] = 1



# =============================================================================
# output
# =============================================================================
df_out.to_csv('output/step3/all.csv',index=False)


# =============================================================================
# additional output without value columns
# =============================================================================
value_columns = [col for col in df_out.columns if "_Value_" in col]
df_out = df_out.drop(columns=value_columns)
df_out.to_csv('output/step3/all_no_value.csv',index=False)

# for measure in ["Value","Quantity","Price"]:
#     temp_measure = ["Year","Month"] + [x for x in df_out.columns if measure in x]
#     df_out[temp_measure].to_csv('output/step3/'+measure+'.csv',index=False)
    