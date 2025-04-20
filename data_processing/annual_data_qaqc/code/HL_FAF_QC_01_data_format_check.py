import pandas as pd
import numpy as np
import HL_FAF_Base_Funtion as hfb

def FAF_QAQC_01_null(df,check_array,outputfile_prefix,check_type):
    outputfile_loc = outputfile_prefix + check_type + ".csv"
    ind = np.isnan(check_array).sum(axis=1)>0
    df_flagged = df.loc[ind]
    if len(df_flagged)>0:
        df_flagged.to_csv(outputfile_loc,index=False)
    return df_flagged

def FAF_QAQC_01_inf(df,check_array,outputfile_prefix,check_type):
    outputfile_loc = outputfile_prefix + check_type + ".csv"
    ind = np.isinf(check_array).sum(axis=1)>0
    df_flagged = df.loc[ind]
    if len(df_flagged)>0:
        df_flagged.to_csv(outputfile_loc,index=False)
    return df_flagged

def FAF_QAQC_01_attribute(df,grp_columns,outputfile_prefix):
    df = df.fillna("")
    df["cnt"] = 1
    df_list_flagged = []
    for col in grp_columns:
        outputfile_loc = outputfile_prefix + "attribute_" + col + ".csv"
        df_mapping = pd.read_excel(hfb.FAF5_metadata_for_mapping_loc,sheet_name=col,dtype=hfb.input_dtype)
        df_grp = df.groupby([col],as_index=False)["cnt"].sum()
        df_grp = df_grp.merge(df_mapping,on=[col],how="outer")
        ind = (df_grp["cnt"].isnull())|(df_grp["_desc_"].isnull())
        ind = ind & (df_grp[col]!="")
        df_flagged = df_grp.loc[ind]
        if len(df_flagged)>0:
            df_flagged.to_csv(outputfile_loc,index=False)
        df_list_flagged = df_list_flagged + [df_flagged]
    return df_list_flagged