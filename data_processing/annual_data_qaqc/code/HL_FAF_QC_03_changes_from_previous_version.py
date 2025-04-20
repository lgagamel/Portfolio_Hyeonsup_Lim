import numpy as np

# =============================================================================
# function to run QA/QC
# =============================================================================
def FAF_QAQC_03(df1,df2,ver1,ver2,year_list,measure,thresholds_by_grp_measure):
    # obtain grp_list and dim_list
    grp_list = list(thresholds_by_grp_measure["grp"])
    grp_list = [x.split("-") for x in grp_list]
    dim_list = list(thresholds_by_grp_measure["dim"])
    
    # obtain measure_columns
    measure_columns = [measure + "_" + y for y in year_list]
    measure_columns = [x for x in measure_columns if x in df1.columns]
    measure_columns1 = [x + "_" + ver1 for x in measure_columns]
    measure_columns2 = [x + "_" + ver2 for x in measure_columns]
    measure_columns_pct = [x+"_dif%" for x in measure_columns]
    measure_columns_dif = [x+"_dif" for x in measure_columns]
    
    # initialize output df_list/df_list_flagged
    df_list = []
    df_list_flagged = []
    for i,grp in enumerate(grp_list):
        thresholds = thresholds_by_grp_measure.iloc[i]
        
        # aggregate and calculate dif/dif%
        df_tmp1 = df1.groupby(grp,as_index=False)[measure_columns].sum()
        df_tmp2 = df2.groupby(grp,as_index=False)[measure_columns].sum()
        df_tmp1.columns = grp + measure_columns1
        df_tmp2.columns = grp + measure_columns2
        df_tmp = df_tmp1.merge(df_tmp2,on=grp,how="outer")
        for col in measure_columns:
            df_tmp[col+"_dif"] = df_tmp[col+ "_" + ver2]-df_tmp[col+ "_" + ver1]
            df_tmp[col+"_dif%"] = df_tmp[col+"_dif"]/df_tmp[col+ "_" + ver1]
        
        pct_array = np.array(df_tmp[measure_columns_pct])
        dif_array = np.array(df_tmp[measure_columns_dif])
        abs_array = np.abs(dif_array)
        
        # flag 1
        ind_1 = np.isinf(pct_array) & (abs_array>thresholds["min_abs"])
        ind_1 = ind_1.sum(axis=1)>0
        df_tmp["flag_1"] = ind_1
        
        # flag 2
        ind_2 = (pct_array>thresholds["max_dif%"]) & (abs_array>thresholds["min_abs"])
        ind_2 = ind_2.sum(axis=1)>0
        df_tmp["flag_2"] = ind_2
        
        # flag 3
        ind_3 = (pct_array<thresholds["min_dif%"]) & (abs_array>thresholds["min_abs"])
        ind_3 = ind_3.sum(axis=1)>0
        df_tmp["flag_3"] = ind_3
        
        # any flagged
        ind_any = ind_1|ind_2|ind_3
        df_tmp["flag_any"] = ind_any
        
        # output
        df_tmp = df_tmp[grp+measure_columns1+measure_columns2+measure_columns_dif+measure_columns_pct+["flag_1","flag_2","flag_3","flag_any"]]
        df_list = df_list + [df_tmp]
        
        # only flagged
        df_tmp = df_tmp.loc[ind_any]
        df_list_flagged = df_list_flagged + [df_tmp]
    return grp_list, dim_list, df_list,df_list_flagged