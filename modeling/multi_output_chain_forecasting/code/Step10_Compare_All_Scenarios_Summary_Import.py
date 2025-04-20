# =============================================================================
# reference
# =============================================================================
# https://medium.com/@josemarcialportilla/using-python-and-auto-arima-to-forecast-seasonal-time-series-90877adff03c
# https://www.datasciencesmachinelearning.com/2019/01/arimasarima-in-python.html
# https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/


# =============================================================================
# library
# =============================================================================
import pandas as pd
from datetime import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
import lzma
import pickle

# =============================================================================
# important parameters
# =============================================================================
total_forecast_n = 15
invasion_end_n = 6
    
# =============================================================================
# load data
# =============================================================================
dtype={"HS":str,"Year":int,"Month":int,"Value":float,"Quantity":float,"Price":float}

df = pd.read_csv('output/step3/all.csv',dtype=dtype)
df_0 = pd.read_csv('output/step7/scenario0/forecast.csv',dtype=dtype)


# =============================================================================
# target_var_list & normalize 
# =============================================================================
target_var_list = [col for col in df.columns if "Import_Value_" in col]
factor = df[target_var_list].iloc[0]
df_0[target_var_list] = df_0[target_var_list] * factor[target_var_list] / 1000000000



# =============================================================================
# filter only 2023
# =============================================================================
ind = df_0["Year"]==2023
df_0 = df_0.loc[ind]



# =============================================================================
# groupby
# =============================================================================
df_0 = df_0.groupby(["Year"],as_index=False)[target_var_list].sum()

df_out = []
for s in ["0","1","2","3","4"]:
    df_s = pd.read_csv('output/step7/scenario'+s+'/forecast.csv',dtype=dtype)
    df_s[target_var_list] = df_s[target_var_list] * factor[target_var_list] / 1000000000
    ind = df_s["Year"]==2023
    df_s = df_s.loc[ind]
    df_s = df_s.groupby(["Year"],as_index=False)[target_var_list].sum()
    total_0 = df_0[target_var_list].sum(axis=1)[0]
    total_s = df_s[target_var_list].sum(axis=1)[0]
    df_out = df_out + [[s,total_0,total_s]]
    
df_out = pd.DataFrame(df_out,columns=["scenario","total_0","total_s"])

# =============================================================================
# output
# =============================================================================
df_out.to_csv('output/step10/import.csv',index=False)