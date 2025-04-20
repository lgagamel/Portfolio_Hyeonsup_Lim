import pandas as pd
from scipy import stats
from scipy.stats import wilcoxon
import numpy as np

df_best = pd.read_csv('output/step_8/1_Summary/summary_only_best.csv')
df = pd.read_csv('output/step_8/1_Summary/performance_all.csv')

df_best = df_best[['measure', 'naics', 'model']]
df_best.columns = ['measure', 'naics', 'best_model']

df = df.merge(df_best,on=['measure', 'naics'],how='left')

df_OLS = df.loc[df['model']=='OLS']
df_best = df.loc[df['model']==df['best_model']]

output = []
for performance_type in ['mae','rmse','r2']:
    for naics in df_OLS['naics'].unique():
        print(naics)
        for measure in ['tons','value']:
            df_OLS_ = df_OLS.copy()
            df_OLS_ = df_OLS_.loc[df_OLS_['performance_type']==performance_type]
            df_OLS_ = df_OLS_.loc[df_OLS_['naics']==naics]
            df_OLS_ = df_OLS_.loc[df_OLS_['measure']==measure]
            
            df_best_ = df_best.copy()
            df_best_ = df_best_.loc[df_best_['performance_type']==performance_type]
            df_best_ = df_best_.loc[df_best_['naics']==naics]
            df_best_ = df_best_.loc[df_best_['measure']==measure]
            
            best_model = df_best_['model'].iloc[0]
            performance_base = df_OLS_['performance'].mean()
            performance_best = df_best_['performance'].mean()
            pct_dif = (performance_best - performance_base)/performance_base
            x = np.array(df_OLS_['performance'])
            y = np.array(df_best_['performance'])
            # raise()
            ttest_result = stats.ttest_rel(x, y)
            if sum(x==y)==len(x):
                wilcoxon_statistic = np.nan
                wilcoxon_pvalue = np.nan
            else:
                wilcoxon_statistic, wilcoxon_pvalue = wilcoxon(x, y)
            tmp_output = [performance_type,naics,measure,best_model,performance_base,performance_best,pct_dif, ttest_result.statistic, ttest_result.pvalue, wilcoxon_statistic, wilcoxon_pvalue]
            output = output + [tmp_output]

df_output = pd.DataFrame(output,columns=['performance_type','naics','measure','best_model','performance_base','performance_best','pct_dif','ttest_statistic', 'ttest_pvalue', 'wilcoxon_statistic', 'wilcoxon_pvalue'])
df_output.to_csv('output/step_8/3_Performance_Comparison/Performance_Comparison.csv',index=False)