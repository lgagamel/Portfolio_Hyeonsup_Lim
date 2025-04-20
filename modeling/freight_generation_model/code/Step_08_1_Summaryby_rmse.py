import pandas as pd
import numpy as np

df_summary = pd.DataFrame()
for model in ['OLS Linear Regression','Lasso','Decision Tree','Random Forest','Gradient Boosting','Support Vector Regression','Gaussian Process','Multilayer Perceptron']:
    df_ = pd.read_csv('output/step_7/'+model+'/summary.csv')
    df_summary = df_summary.append(df_)


df_summary['model'] = df_summary['model'].replace({'OLS Linear Regression':'OLS',
                                                   'Linear Regression (OLS)':'OLS',
          'Lasso':'Lasso',
          'Decision Tree':'DTR',
          'Random Forest':'RFR',
          'Gradient Boosting':'GBR',
          'Support Vector Regression':'SVR',
          'Gaussian Process':'GPR',
          'Multilayer Perceptron':'MPR',
          '':'',})
    
df_summary.to_csv('output/step_8/1_Summary/summary.csv',index=False)

df_summary_pivot = pd.pivot_table(df_summary, values='rmse', index=['measure', 'naics'],
                    columns=['model'], aggfunc=np.sum, fill_value=0)


df_summary_pivot.to_csv('output/step_8/1_Summary/summary_mae_by_model.csv')

df_summary_ = df_summary.groupby(['measure','naics'],as_index=False)['rmse'].min()
df_summary_.columns = ['measure','naics','rmse_min']


df_summary_OLS = df_summary.loc[df_summary["model"]=="OLS"].copy()
df_summary_OLS = df_summary_OLS.groupby(['measure','naics'],as_index=False)['rmse'].min()
df_summary_OLS.columns = ['measure','naics','rmse_OLS']


df_summary = df_summary.merge(df_summary_,on=['measure','naics'],how='left')
df_summary = df_summary.merge(df_summary_OLS,on=['measure','naics'],how='left')

df_summary = df_summary.loc[df_summary['rmse'] == df_summary['rmse_min']]

ind = df_summary['model'] != "OLS"
ind = ind & (df_summary['rmse_min']==df_summary['rmse_OLS'])
df_summary = df_summary.loc[~ind]
df_summary.to_csv('output/step_8/1_Summary/summary_only_best_all.csv',index=False)
df_summary = df_summary[['measure','naics','model','mae','r2', 'rmse']]
df_summary.to_csv('output/step_8/1_Summary/summary_only_best.csv',index=False)