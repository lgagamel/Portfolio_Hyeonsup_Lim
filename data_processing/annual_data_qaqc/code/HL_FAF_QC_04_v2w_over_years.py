import numpy as np

# =============================================================================
# function to run QA/QC
# =============================================================================
def FAF_QAQC_04(df,year_list,thresholds_by_grp_measure):
    # obtain grp_list and dim_list
    grp_list = list(thresholds_by_grp_measure["grp"])
    grp_list = [x.split("-") for x in grp_list]
    dim_list = list(thresholds_by_grp_measure["dim"])
    
    # obtain measure_columns
    measure_columns_tons = ["tons_" + y for y in year_list]
    measure_columns_tons = [x for x in measure_columns_tons if x in df.columns]
    measure_columns_value = ["value_" + y for y in year_list]
    measure_columns_value = [x for x in measure_columns_value if x in df.columns]
    measure_columns_v2w = [x.replace("tons_","v2w_") for x in measure_columns_tons]
    measure_columns_pct = [x+"_dif%" for x in measure_columns_v2w]
    measure_columns_dif = [x+"_dif" for x in measure_columns_v2w]
    
    # initialize output df_list/df_list_flagged
    df_list = []
    df_list_flagged = []
    for i,grp in enumerate(grp_list):
        thresholds = thresholds_by_grp_measure.iloc[i]
        
        # aggregate and calculate dif/dif%
        df_tmp = df.groupby(grp,as_index=False)[measure_columns_tons+measure_columns_value].sum()
        df_tmp.loc[:,measure_columns_v2w] = np.array(df_tmp[measure_columns_value])/np.array(df_tmp[measure_columns_tons])/2
        prev_col = measure_columns_v2w[0]
        for col in measure_columns_v2w:
            df_tmp[col+"_dif"] = df_tmp[col]-df_tmp[prev_col]
            df_tmp[col+"_dif%"] = df_tmp[col+"_dif"]/df_tmp[prev_col]
            prev_col = col
        
        pct_array = np.array(df_tmp[measure_columns_pct])
        dif_array = np.array(df_tmp[measure_columns_dif])
        abs_array = np.abs(dif_array)
        tons_array = np.array(df_tmp[measure_columns_tons])
        value_array = np.array(df_tmp[measure_columns_value])
        
        # flag 1
        ind_1 = np.isinf(pct_array) & (abs_array>thresholds["min_abs"]) & ((tons_array>thresholds["min_tons"]) | (value_array>thresholds["min_value"]))
        ind_1 = ind_1.sum(axis=1)>0
        df_tmp["flag_1"] = ind_1
        
        # flag 2
        ind_2 = (pct_array>thresholds["max_dif%"]) & (abs_array>thresholds["min_abs"]) & ((tons_array>thresholds["min_tons"]) | (value_array>thresholds["min_value"]))
        ind_2 = ind_2.sum(axis=1)>0
        df_tmp["flag_2"] = ind_2
        
        # flag 3
        ind_3 = (pct_array<thresholds["min_dif%"]) & (abs_array>thresholds["min_abs"]) & ((tons_array>thresholds["min_tons"]) | (value_array>thresholds["min_value"]))
        ind_3 = ind_3.sum(axis=1)>0
        df_tmp["flag_3"] = ind_3
        
        # any flagged
        ind_any = ind_1|ind_2|ind_3
        df_tmp["flag_any"] = ind_any
        
        # output
        df_tmp = df_tmp[grp+measure_columns_tons+measure_columns_value+measure_columns_v2w+measure_columns_dif+measure_columns_pct+["flag_1","flag_2","flag_3","flag_any"]]
        df_list = df_list + [df_tmp]
        
        # only flagged
        df_tmp = df_tmp.loc[ind_any]
        df_list_flagged = df_list_flagged + [df_tmp]
    return grp_list, dim_list, df_list,df_list_flagged