import pandas as pd
import numpy as np

df_summary = pd.DataFrame()
for model in ['OLS Linear Regression','Lasso','Decision Tree','Random Forest','Gradient Boosting','Support Vector Regression','Gaussian Process','Multilayer Perceptron']:
    df_ = pd.read_csv('output/step_7/'+model+'/all.csv')
    df_summary = df_summary.append(df_)


df_summary['model'] = df_summary['model'].replace({'OLS Linear Regression':'OLS',
          'Lasso':'Lasso',
          'Decision Tree':'DTR',
          'Random Forest':'RFR',
          'Gradient Boosting':'GBR',
          'Support Vector Regression':'SVR',
          'Gaussian Process':'GPR',
          'Multilayer Perceptron':'MPR',
          '':'',})
    
df_summary.to_csv('output/step_8/1_Summary/all.csv',index=False)