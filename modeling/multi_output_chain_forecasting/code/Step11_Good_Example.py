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
import os

# =============================================================================
# load data
# =============================================================================
dtype={"HS":str,"Year":int,"Month":int,"Value":float,"Quantity":float,"Price":float}

df_HS_list = pd.read_csv('input/impacted_HS/major_impacted_HS.csv',dtype=dtype)


# =============================================================================
# check impacted HS list
# =============================================================================
HS_list = [x[:4] for x in df_HS_list["HS"]]



file_list = os.listdir("output/step6/cross_corr_by_HS/")
candidate_list = []
for filename in file_list:
    df_cross_corr = pd.read_csv("output/step6/cross_corr_by_HS/"+filename)
    df_cross_corr["upstream_var_HS"] = df_cross_corr["upstream_var"].apply(lambda x: x[-4:])
    if sum(df_cross_corr["upstream_var_HS"].isin(HS_list))>0:
        candidate_list = candidate_list + [filename.replace(".csv","")]
        df_cross_corr.to_csv("output/step11/cross_corr_by_HS/"+filename,index=False)


# =============================================================================
# check model performance
# =============================================================================
df_performance = pd.read_csv('output/step8/comparison.csv',dtype=dtype)
ind = df_performance["target"].isin(candidate_list)
df_performance.loc[ind].to_csv('output/step11/comparison_selected1.csv',index=False)

            