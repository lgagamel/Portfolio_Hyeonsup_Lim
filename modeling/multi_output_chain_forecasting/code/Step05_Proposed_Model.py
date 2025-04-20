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

# =============================================================================
# important parameters
# =============================================================================
total_forecast_n = 15
invasion_end_n = 6

# =============================================================================
# check differencing (d)
# =============================================================================
def find_best_d(df):
    best_d = 0
    df_diff = df.copy()
    result = adfuller(df_diff)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    p_value = result[1]
    
    while p_value>0.05:
        best_d = best_d + 1
        df_diff = df_diff.diff().dropna()
        result = adfuller(df_diff)    
        p_value = result[1]
    
    print(best_d)
    return best_d

# =============================================================================
# accuracy
# =============================================================================
# Accuracy metrics
def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    r2 = corr**2
    return [mape,me,mae,mpe,rmse,corr,r2]
    # return({'mape':mape, 'me':me, 'mae': mae, 'mpe': mpe, 'rmse':rmse,'corr':corr,'r2':r2})

# =============================================================================
# calculate cross correlation
# =============================================================================
def get_max_cross_correlation(df,target_var,upstream_var,best_d):
    # =============================================================================
    # based on best d
    # =============================================================================
    A = df[target_var]
    B = df[upstream_var]
    
    for i in range(best_d):
        A = A.diff()
        B = B.diff()
    A = A.dropna()
    B = B.dropna()
    
    # =============================================================================
    # check
    # =============================================================================
    r2_max = 0
    i_opt = 0
    for j in range(12):
        i = j + 1
        corr = np.corrcoef(A[i:], B[:-i])[0,1]
        r2 = corr**2
        if r2>r2_max:
            i_opt = i
            r2_max = r2
    return i_opt,r2_max
    
# =============================================================================
# load data
# =============================================================================
dtype={"HS":str,"Year":int,"Month":int,"Value":float,"Quantity":float,"Price":float}

df = pd.read_csv('output/step3/all.csv',dtype=dtype)

# =============================================================================
# output summary
# =============================================================================
f = open("output/step5/summary.csv","w")
f.write(",".join(["target","mape","me","mae","mpe","rmse","corr","r2"]))
f.write("\n")

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

df_forecast = df.copy()
# =============================================================================
# Main Loop
# =============================================================================
for i,target_var in enumerate(target_var_list):
    try:
        print(i,target_var)
        # =============================================================================
        # for test
        # =============================================================================
        # df[target_var] = df[target_var]/df.loc["2002-01-01",target_var]
        df_temp = df[[target_var,"Recession","Invasion","Covid","Suez","Freeze"]].copy()
        
        # =============================================================================
        # decomposition
        # =============================================================================
        # result = seasonal_decompose(df_temp, model="multiplicative")
        # result = seasonal_decompose(df_temp, model="additive")
        # fig = result.plot()
        
        best_d = find_best_d(df_temp[target_var])
        
        # =============================================================================
        # cross-correlation
        # =============================================================================
        # value_col_list = [col for col in df.columns if ("_Value_" in col)&(col!=target_var)]
        cross_corr = []
        for upstream_var in target_var_list:    
            if target_var!=upstream_var:
                i_opt,r2_max = get_max_cross_correlation(df,target_var,upstream_var,best_d)
                cross_corr = cross_corr + [[upstream_var,i_opt,r2_max]]
        df_cross_corr = pd.DataFrame(cross_corr,columns=["upstream_var","i_opt","r2_max"])
        df_cross_corr = df_cross_corr.sort_values(by="r2_max",ascending=False)

        df_cross_corr.iloc[:20].to_csv("output/step5/cross_corr_by_HS/"+target_var+".csv",index=False)
        
        # =============================================================================
        # sub columns
        # =============================================================================
        for i in range(5):
            upstream_var = df_cross_corr.iloc[i]["upstream_var"]
            i_opt = df_cross_corr.iloc[i]["i_opt"]
            r2_max = df_cross_corr.iloc[i]["r2_max"]
            
            B = df[upstream_var]
            for i in range(best_d):
                B = B.diff()
            
            B = np.array(B[:-i_opt])
            dummy_array = np.zeros(i_opt)
            dummy_array[:]=np.nan
            df_temp[upstream_var] = np.concatenate([dummy_array,B])
        df_temp = df_temp.dropna()
        
        # =============================================================================
        # split train test
        # =============================================================================
        train = df_temp.loc['2002-01-01':'2022-03-01']
        test = df_temp.loc['2022-04-01':]
        
        
        
        # =============================================================================
        # auto arima
        # =============================================================================
        # best_d = find_best_d(df[target_var])
        stepwise_model = auto_arima(train[[target_var]], 
                                    exogenous=train[["Recession","Invasion","Covid","Suez","Freeze"]], 
                                    # d=None, max_d=2, 
                                    d=best_d,
                                    start_p=2, max_p=5, 
                                    start_q=2, max_q=5,
                                    D=None, max_D=2,
                                    # D=1,
                                    start_P=2, max_P=3, 
                                    start_Q=2, max_Q=3,
                                    m=12,seasonal=True,
                                    trace=True,error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True,
                                    with_intercept=True,
                                    information_criterion="aicc",
                                    test = "adf",
                                    maxiter=50)
        
        # print(stepwise_model.aic())
        # print(stepwise_model.summary())
        # stepwise_model.pvalues()["Invasion"]
        # stepwise_model.pvalues()["Export_Price_9617002000"]
        
        # =============================================================================
        # model diagnostics
        # =============================================================================
        # stepwise_model.plot_diagnostics(figsize=(7,7))
        # plt.show()
        
        # =============================================================================
        # train model
        # =============================================================================
        best_aic = stepwise_model.aic()
        best_aicc = stepwise_model.aicc()
        best_bic = stepwise_model.bic()
        best_infc = np.array([best_aic,best_aicc,best_bic])
        
        best_i = 0
        for i in range(5):
            extra_columns = list(df_cross_corr.iloc[:i+1]["upstream_var"])    
            stepwise_model.fit(train[[target_var]], 
                               exogenous=train[["Recession","Invasion","Covid","Suez","Freeze"]+extra_columns])
            current_aic = stepwise_model.aic()
            current_aicc = stepwise_model.aicc()
            current_bic = stepwise_model.bic()
            current_infc = np.array([current_aic,current_aicc,current_bic])
            print(i,sum(current_infc<best_infc)) 
            if sum(current_infc<best_infc)>=3:
                best_infc = current_infc.copy()
                best_i = i+1
            else:
                break

        # =============================================================================
        # final fitting
        # =============================================================================
        best_extra_columns = list(df_cross_corr.iloc[:best_i]["upstream_var"])  
        stepwise_model.fit(train[[target_var]], 
                           exogenous=train[["Recession","Invasion","Covid","Suez","Freeze"]+best_extra_columns])


        # =============================================================================
        # evaluation
        # =============================================================================
        val_est,confint = stepwise_model.predict(n_periods=len(test), 
                                                          exogenous=test[["Recession","Invasion","Covid","Suez","Freeze"]+best_extra_columns], 
                                                         return_conf_int=True)
        # val_est = pd.Series(val_est, index=test.index)
        lower_series = pd.Series(confint[:, 0], index=test.index)
        upper_series = pd.Series(confint[:, 1], index=test.index)
        
        
        # =============================================================================
        # # Plot
        # =============================================================================
        # plt.plot(train.loc['2018-01-01':,target_var],label="train")
        # # plt.plot(train[target_var],label="train")
        # plt.plot(test[target_var],label="test")
        # plt.plot(val_est,label="val_est")
        # plt.fill_between(lower_series.index, 
        #                   lower_series, 
        #                   upper_series, 
        #                   color='k', alpha=.15,label="confidence_interval")
        # plt.title("Final Forecast")
        # plt.legend()
        # plt.show()
        
        # =============================================================================
        # add forecast
        # =============================================================================
        df_temp["val_est"] = np.nan
        df_temp["val_est_lower"] = np.nan
        df_temp["val_est_upper"] = np.nan
        df_temp["val_est"][-len(val_est):] = np.array(val_est)
        df_temp["val_est_lower"][-len(lower_series):] = np.array(lower_series)
        df_temp["val_est_upper"][-len(upper_series):] = np.array(upper_series)
        
        
        # =============================================================================
        # write accuracy to summary
        # =============================================================================
        model_performance = forecast_accuracy(np.array(val_est), np.array(test[target_var]))
        model_performance = [str(x) for x in model_performance]
        f.write(",".join([target_var]+model_performance))
        f.write("\n")
        
        
        # =============================================================================
        # write result for target_val
        # =============================================================================
        num_col_list = [target_var,"val_est","val_est_lower","val_est_upper"]
        for col in num_col_list:
            df_temp[col] = df_temp[col] * target_factor[target_var]
        df_temp.to_csv("output/step5/by_HS/"+target_var+".csv")
        
        
        
        
        # =============================================================================
        # output
        # =============================================================================
        # df_out = pd.concat([train[target_var],test[target_var],future_forecast],axis=1)
        # df_out.columns=["train","test","predicted"]
        # df_out.to_csv("output/step5/target_var/"+target_var+".csv")
    except:
        pass
f.close()