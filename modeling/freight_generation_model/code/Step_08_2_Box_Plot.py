import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt

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
            df_.columns = ['mae']
            df_['model'] = model
            df_['measure'] = measure
            df_['naics'] = naics
            #print(model,measure,naics)
            df_summary = df_summary.append(df_)




df_summary_OLS = df_summary.loc[df_summary['model']=='OLS Linear Regression']
df_summary_OLS = df_summary_OLS.groupby(['measure','model','naics'],as_index=False)['mae'].mean()
df_summary_OLS = df_summary_OLS.rename(columns={'mae':'mae_OLS'})

df_summary = df_summary.merge(df_summary_OLS[['measure','naics','mae_OLS']],on=['measure','naics'],how='left')
df_summary['relative_mae'] = df_summary['mae']/df_summary['mae_OLS']

df_summary.to_csv('output/step_8/test.csv',index=False)


g = sns.catplot(x="measure", y="relative_mae",
                hue="model", col="naics",col_wrap = 4,
                data=df_summary, kind="box", legend=False,
                height=4, aspect=1);
plt.ylim([0,2])
plt.legend(loc='lower center', bbox_to_anchor=(-1.2, -0.25),
          fancybox=True, shadow=True, ncol=8)

g.savefig("output/step_8/all.png")

for naics in df_summary.naics.unique():
    df = df_summary.loc[(df_summary['naics']==naics)]
    ax = sns.boxplot(x="measure", y="relative_mae",hue="model", data=df)
    #ax = sns.swarmplot(x="measure", y="relative_mae",hue="model", data=df, color=".25")
    ax.get_legend().remove()
    plt.ylim([0,2])
    plt.tight_layout()
    plt.savefig("output/step_8/by_naics/"+naics+".png")
    
    plt.show()

ax = sns.boxplot(x="measure", y="relative_mae",hue="model", data=df)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
#plt.xlim([-1,100])
plt.ylim([-1,0])
#plt.tight_layout()
plt.savefig("output/step_8/by_naics/legend.png", dpi=800, pad_inches=2000)
plt.show()