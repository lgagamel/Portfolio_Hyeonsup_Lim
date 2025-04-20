# =============================================================================
# reference
# =============================================================================
# https://medium.com/@josemarcialportilla/using-python-and-auto-arima-to-forecast-seasonal-time-series-90877adff03c
# https://www.datasciencesmachinelearning.com/2019/01/arimasarima-in-python.html
# https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/

import pandas as pd


# =============================================================================
# load data
# =============================================================================
df_simple = pd.read_csv("output/step4/summary.csv")
df_proposed = pd.read_csv("output/step5/summary.csv")

# =============================================================================
# drop duplicates
# =============================================================================
df_simple = df_simple.drop_duplicates()
df_proposed = df_proposed.drop_duplicates()

# =============================================================================
# change column names
# =============================================================================
columns_to_be_changed = list(df_simple.columns)
columns_to_be_changed = columns_to_be_changed[1:]
for col in columns_to_be_changed:
    df_simple = df_simple.rename(columns={col:col+"_simple"})
    df_proposed = df_proposed.rename(columns={col:col+"_proposed"})


# =============================================================================
# merge
# =============================================================================
df = df_simple.merge(df_proposed,on=["target"],how="inner")


# =============================================================================
# output
# =============================================================================
df.to_csv("output/step8/comparison_inner.csv",index=False)
