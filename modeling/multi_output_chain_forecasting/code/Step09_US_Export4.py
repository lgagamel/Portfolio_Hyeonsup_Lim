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
df_forecast = pd.read_csv('output/step7/scenario4/forecast.csv',dtype=dtype)
df_std = pd.read_csv('output/step7/scenario4/forecast_std_err.csv',dtype=dtype)
# =============================================================================
# index time
# =============================================================================
df["Time"] = df.apply(lambda x: datetime(int(x["Year"]), int(x["Month"]),1),axis=1)
df = df.set_index("Time")

# =============================================================================
# target_var_list & normalize 
# =============================================================================
target_var_list = [col for col in df.columns if "Export_Value_" in col]
factor = df[target_var_list].iloc[0]

# =============================================================================
# remove null col
# =============================================================================
for col in target_var_list:
    ind1 = sum(df_forecast[col].isnull())
    ind2 = sum(df_std[col].isnull())
    if (ind1|ind2):
        print(col)
        target_var_list.remove(col)


# =============================================================================
# select forecast part only
# =============================================================================
ind = df_forecast["forecast"]==1
df_observed = df_forecast.loc[~ind].copy()
df_forecast = df_forecast.loc[ind].copy()

# =============================================================================
# calculate df_observed
# =============================================================================
df_observed[target_var_list] = df_observed[target_var_list] * factor[target_var_list] / 1000000000
df_observed["observed"] = df_observed[target_var_list].sum(axis=1)
df_observed = df_observed[["Year","Month","observed"]]

# =============================================================================
# convert to original unit
# =============================================================================
df_forecast[target_var_list] = df_forecast[target_var_list] * factor[target_var_list] / 1000000000
df_std[target_var_list] = df_std[target_var_list] * factor[target_var_list] / 1000000000

# =============================================================================
# loop
# =============================================================================
output = []
for i in range(len(df_forecast)):
    mean = np.array(df_forecast.iloc[i][target_var_list])
    std = np.array(df_std.iloc[i][target_var_list])
    
    est = np.random.normal(loc=mean, scale=std,size=(1000,len(mean)))
    est = np.sum(est, axis=1)
    est_mean = np.mean(est)
    est_median = np.percentile(est, 50, axis=0)
    est_low = np.percentile(est, 5, axis=0)
    est_high = np.percentile(est, 95, axis=0)
    output = output + [[est_mean,est_median,est_low,est_high]]

df_out = pd.DataFrame(output,columns=["mean","median","low","high"])
df_out["Year"] = np.array(df_forecast["Year"])
df_out["Month"] = np.array(df_forecast["Month"])



# =============================================================================
# output
# =============================================================================
df_out = df_out[["Year","Month","mean","median","low","high"]]
df_out = df_observed.append(df_out)
df_out.to_csv('output/step9/scenario4/us_export_forecast.csv',index=False)
            