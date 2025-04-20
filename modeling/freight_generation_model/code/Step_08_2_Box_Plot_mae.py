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
            df_.columns = ['mae']
            df_['model'] = model
            df_['measure'] = measure
            df_['naics'] = naics
            #print(model,measure,naics)
            df_summary = df_summary.append(df_)


df_summary['model'] = df_summary['model'].replace({'OLS Linear Regression':'OLS',
          'Lasso':'Lasso',
          'Decision Tree':'DTR',
          'Random Forest':'RFR',
          'Gradient Boosting':'GBR',
          'Support Vector Regression':'SVR',
          'Gaussian Process':'GPR',
          'Multilayer Perceptron':'MLP',
          '':'',})


df_summary_OLS = df_summary.loc[df_summary['model']=='OLS']
df_summary_OLS = df_summary_OLS.groupby(['measure','model','naics'],as_index=False)['mae'].mean()
df_summary_OLS = df_summary_OLS.rename(columns={'mae':'mae_OLS'})

df_summary = df_summary.merge(df_summary_OLS[['measure','naics','mae_OLS']],on=['measure','naics'],how='left')
df_summary['Relative MAE (compared to OLS)'] = (df_summary['mae']/df_summary['mae_OLS'] - 1)*100
df_summary['mae'] = df_summary['mae']/1000

df_summary.to_csv('output/step_8/2_Box_Plot/mae/all.csv',index=False)


g = sns.catplot(x="measure", y="Relative MAE (compared to OLS)",
                hue="model", col="naics",col_wrap = 4,
                data=df_summary, kind="box", legend=False,
                height=4, aspect=1);
#g.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.ylim([-100,100])
plt.legend(loc='lower center', bbox_to_anchor=(-1.2, -0.25),
          fancybox=True, shadow=True, ncol=8)

plt.savefig("output/step_8/2_Box_Plot/mae/all.png",dpi=1000)
plt.show()


for measure in ['tons','value']:
    for naics in df_summary.naics.unique():
        df = df_summary.loc[(df_summary['naics']==naics)&(df_summary['measure']==measure)]
        plt.plot([-20,20], [0,0],'k:', linewidth=3)
        ax = sns.boxplot(x="model", y="Relative MAE (compared to OLS)", data=df, width=0.3)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        #ax = sns.swarmplot(x="measure", y="mae",hue="model", data=df, color=".25")
        #ax.get_legend().remove()
        plt.ylim([-100,100])
        plt.tight_layout()
        plt.xlabel(None)
        #plt.plot([-20,0.5], [-85,-85],'k:', linewidth=3)
        # plt.annotate('Avg. MAE by OLS', xy=(-0.4, +3), fontsize=8, fontweight='bold')
        plt.savefig("output/step_8/2_Box_Plot/mae/by_naics/"+ measure+"_"+naics+".png",dpi=500)
        
        plt.show()

ax = sns.boxplot(x="measure", y="mae",hue="model", data=df)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
#plt.xlim([-1,100])
plt.ylim([-1,0])
#plt.tight_layout()
plt.savefig("output/step_8/2_Box_Plot/mae/by_naics/legend.png", dpi=800, pad_inches=2000)
plt.show()