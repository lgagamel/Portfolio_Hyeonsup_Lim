import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
#import matplotlib

plt.rcParams.update({'font.size': 15})

df_summary = pd.DataFrame()
for model in ['OLS Linear Regression','Lasso','Decision Tree','Random Forest','Gradient Boosting','Support Vector Regression','Gaussian Process','Multilayer Perceptron']:
    folder = 'output/step_7/'+model+'/by_naics'
    filelist = os.listdir('output/step_7/'+model+'/by_naics')
    for file in filelist:
        if 'mae' in file:
            file_to_list = file.split('_')
            measure = file_to_list[0]
            naics = file_to_list[1]
            df_ = pd.read_csv(folder+'/'+file,header=None)
            df_.columns = ['performance']
            df_['model'] = model
            df_['measure'] = measure
            df_['naics'] = naics
            df_['performance_type'] = 'mae'
            #print(model,measure,naics)
            df_summary = df_summary.append(df_)
            
        if 'rmse' in file:
            file_to_list = file.split('_')
            measure = file_to_list[0]
            naics = file_to_list[1]
            df_ = pd.read_csv(folder+'/'+file,header=None)
            df_.columns = ['performance']
            df_['model'] = model
            df_['measure'] = measure
            df_['naics'] = naics
            df_['performance_type'] = 'rmse'
            #print(model,measure,naics)
            df_summary = df_summary.append(df_)
            
        if 'r2' in file:
            file_to_list = file.split('_')
            measure = file_to_list[0]
            naics = file_to_list[1]
            df_ = pd.read_csv(folder+'/'+file,header=None)
            df_.columns = ['performance']
            df_['model'] = model
            df_['measure'] = measure
            df_['naics'] = naics
            df_['performance_type'] = 'r2'
            #print(model,measure,naics)
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


df_summary= df_summary[['measure','naics','model','performance_type','performance']]
df_summary.to_csv('output/step_8/1_Summary/performance_all.csv',index=False)