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
df_4 = pd.read_csv('output/step7/scenario4/forecast.csv',dtype=dtype)

# =============================================================================
# target_var_list & normalize 
# =============================================================================
target_var_list = [col for col in df.columns if "Export_Value_" in col]
factor = df[target_var_list].iloc[0]
df_0[target_var_list] = df_0[target_var_list] * factor[target_var_list] / 1000000000
df_4[target_var_list] = df_4[target_var_list] * factor[target_var_list] / 1000000000


# =============================================================================
# filter only 2023
# =============================================================================
ind = df_0["Year"]==2023
df_0 = df_0.loc[ind]

ind = df_4["Year"]==2023
df_4 = df_4.loc[ind]


# =============================================================================
# groupby
# =============================================================================
df_0 = df_0.groupby(["Year"],as_index=False)[target_var_list].sum()
df_4 = df_4.groupby(["Year"],as_index=False)[target_var_list].sum()


# =============================================================================
# Merge
# =============================================================================
df_diff = df_4-df_0
df_pct_diff = df_diff/df_0


# =============================================================================
# output
# =============================================================================
df_0.to_csv('output/step10/export/df_0.csv',index=False)
df_4.to_csv('output/step10/export/df_4.csv',index=False)
df_diff.to_csv('output/step10/export/df_diff.csv',index=False)
df_pct_diff.to_csv('output/step10/export/df_pct_diff.csv',index=False)
            