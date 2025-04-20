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
# =============================================================================
# index time
# =============================================================================
df["Time"] = df.apply(lambda x: datetime(int(x["Year"]), int(x["Month"]),1),axis=1)
df_out = df[["Time"]].copy()
df = df.set_index("Time")

# =============================================================================
# target_var_list & normalize 
# =============================================================================
target_var_list = [col for col in df.columns if "Export_Value_" in col]
observed = np.zeros(len(df))
model1 = np.zeros(len(df))
model2 = np.zeros(len(df))
for target_var in target_var_list:
    try:
        df1 = pd.read_csv("output/step4/by_HS/"+target_var+".csv")
        df1 = df1.set_index("Time")
        
        df2 = pd.read_csv("output/step5/by_HS/"+target_var+".csv")
        df2 = df2.set_index("Time")
        
        observed = observed + np.array(df1.loc[:"2022-09-01"][target_var])/1000000
        
        df1 = df1.loc["2022-04-01":"2022-09-01"]
        model1_tmp = np.zeros(len(df))
        model1_est = np.array(df1["val_est"])/1000000
        model1_tmp[-len(model1_est):] = model1_est        
        
        df2 = df2.loc["2022-04-01":"2022-09-01"]        
        model2_tmp = np.zeros(len(df))
        model2_est = np.array(df2["val_est"])/1000000
        model2_tmp[-len(model2_est):] = model2_est    
        
        model1 = model1 + model1_tmp
        model2 = model2 + model2_tmp
        print(target_var)
    except:
        pass
    
df_out["observed"] = observed
df_out["model1"] = model1
df_out["model2"] = model2

# =============================================================================
# output
# =============================================================================
df_out.to_csv('output/step12/us_export_value.csv',index=False)
            