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
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from dateutil.relativedelta import relativedelta
import lzma
import pickle

# =============================================================================
# important parameters
# =============================================================================
total_forecast_n = 15
invasion_end_n = 12
    
# =============================================================================
# load data
# =============================================================================
dtype={"HS":str,"Year":int,"Month":int,"Value":float,"Quantity":float,"Price":float}

df = pd.read_csv('output/step3/all.csv',dtype=dtype)
train_n = len(df)

# =============================================================================
# index time
# =============================================================================
df["Time"] = df.apply(lambda x: datetime(int(x["Year"]), int(x["Month"]),1),axis=1)
df = df.set_index("Time")

# =============================================================================
# target_var_list & normalize 
# =============================================================================
target_var_list = [col for col in df.columns if "_Value_" in col]
target_factor = df[target_var_list].iloc[0].copy()
df[target_var_list] = df[target_var_list]/df[target_var_list].iloc[0]
df["forecast"] = 0

# =============================================================================
# additional outputs for confidence interval
# =============================================================================
df_lower = df.copy()
df_lower = df_lower.iloc[0:0]
df_upper = df_lower.copy()

# =============================================================================
# add next month
# =============================================================================
current_month = df.index[-1]
for forecast_i in range(total_forecast_n):
    next_month = (current_month + relativedelta(months=+1))
    df.loc[next_month,:] = df.loc[current_month,:]
    if forecast_i<invasion_end_n:
        df.loc[next_month,"Invasion"]=1
    else:
        df.loc[next_month,"Invasion"]=0
    df.loc[next_month,target_var_list]=np.nan
    df.loc[next_month,"forecast"]=1
    current_month = next_month
    
    # =============================================================================
    # Main Loop
    # =============================================================================
    for target_var_i,target_var in enumerate(target_var_list):
        try:
            print(forecast_i,target_var_i,target_var)
            
            # =============================================================================
            # load df_cross_corr best_extra_columns
            # =============================================================================
            df_cross_corr = pd.read_csv("output/step6/cross_corr_by_HS/"+target_var+".csv")
            best_extra_columns = list(df_cross_corr["upstream_var"])
            
            # =============================================================================
            # load model
            # =============================================================================
            with lzma.open('output/step6/model_by_HS/'+target_var+'.lzma','rb') as f:
                stepwise_model_test = pickle.load(f)
                
            best_d = stepwise_model_test.order[1]
            
            # =============================================================================
            # for test
            # =============================================================================
            # df[target_var] = df[target_var]/df.loc["2002-01-01",target_var]
            df_temp = df[[target_var,"Recession","Invasion","Covid","Suez","Freeze"]+best_extra_columns].copy()
            
            # =============================================================================
            # fitting again - removed
            # =============================================================================
            # df_train = df_temp.iloc[:train_n].copy()
            # stepwise_model_test.fit(df_train[[target_var]], 
            #                    exogenous=df_train[["Recession","Invasion","Covid","Suez","Freeze"]+best_extra_columns])
            
            
            # =============================================================================
            # sub columns
            # =============================================================================
            for i in range(len(df_cross_corr)):
                upstream_var = df_cross_corr.iloc[i]["upstream_var"]
                i_opt = df_cross_corr.iloc[i]["i_opt"]
                r2_max = df_cross_corr.iloc[i]["r2_max"]
                
                B = df_temp[upstream_var]
                for i in range(best_d):
                    B = B.diff()
                
                B = np.array(B[:-i_opt])
                dummy_array = np.zeros(i_opt)
                dummy_array[:]=np.nan            
                df_temp[upstream_var] = np.concatenate([dummy_array,B])
            # df_temp = df_temp.dropna()
            X = df_temp.drop(columns=[target_var])
            X = np.array(X.iloc[-forecast_i-1:])
            # if forecast_i==0:
            #     X = np.array([X.iloc[-forecast_i-1:]])
            # else:
            #     X = np.array(X.iloc[-forecast_i-1:])
            
            # =============================================================================
            # predict future
            # =============================================================================
            val_est,confint = stepwise_model_test.predict(n_periods=forecast_i+1,exogenous=X, 
                                                             return_conf_int=True,alpha=0.05)
            
            
            df.loc[current_month,"Year"]=current_month.year
            df.loc[current_month,"Month"]=current_month.month
            df.loc[current_month,target_var]=val_est[-1]
            
            df_lower.loc[current_month,"Year"]=current_month.year
            df_lower.loc[current_month,"Month"]=current_month.month
            df_lower.loc[current_month,target_var]=confint[-1, 0]
            
            df_upper.loc[current_month,"Year"]=current_month.year
            df_upper.loc[current_month,"Month"]=current_month.month
            df_upper.loc[current_month,target_var]=confint[-1, 1]
        except:
            pass
        
        
        
# =============================================================================
# standard error
# =============================================================================
df_std_error = (df_upper - df_lower)/2/1.96


# =============================================================================
# output
# =============================================================================
df.to_csv('output/step7/scenario3/forecast.csv',index=False)
df_lower.to_csv('output/step7/scenario3/forecast_lower.csv',index=False)
df_upper.to_csv('output/step7/scenario3/forecast_upper.csv',index=False)
df_std_error.to_csv('output/step7/scenario3/forecast_std_err.csv',index=False)
        
            