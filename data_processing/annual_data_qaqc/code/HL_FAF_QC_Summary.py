import pandas as pd
import os

def FAF_QAQC_Summary(df_list_flagged,grp_list,qaqc_name,dim_list,measure):
    summary_loc = "output/summary.csv"
    summary = []
    for i,df in enumerate(df_list_flagged):
        grp = grp_list[i]
        dim = str(dim_list[i])
        grp_name = '-'.join(grp)
        N_flag = str(len(df))
        summary_tmp = [qaqc_name,dim,measure,grp_name,N_flag]
        summary = summary + [summary_tmp]
    df_summary = pd.DataFrame(summary,columns=["check","dim","measure","group","N_flag"])
    if os.path.exists(summary_loc):
        df_summary.to_csv(summary_loc,index=False,mode="a",header=None)
    else:
        df_summary.to_csv(summary_loc,index=False)