# =============================================================================
# Library
# =============================================================================
import pandas as pd
import numpy as np

# custome by HL
import HL_FAF_Base_Funtion as hfb
from HL_FAF_QC_01_data_format_check import FAF_QAQC_01_null, FAF_QAQC_01_inf, FAF_QAQC_01_attribute
from HL_FAF_QC_Summary import FAF_QAQC_Summary

# =============================================================================
# user input
# =============================================================================
qaqc_name = "01_data_format_check"
target_version = hfb.target_version

# =============================================================================
# read data
# =============================================================================
year_list = hfb.year_list
inputfile_loc = hfb.inputfile_loc_by_version[hfb.target_version]
df = pd.read_csv(inputfile_loc,dtype=hfb.input_dtype)

# check only measure (tons, value, tmiles) columns
grp_columns = hfb.key_columns
grp_columns = [x for x in df.columns if x in grp_columns]
measure_columns = [x for x in df.columns if x not in grp_columns]
check_array = np.array(df[measure_columns])


# =============================================================================
# check null/inf
# =============================================================================
dim_list = ["full"]
outputfile_prefix = 'output/only_flagged/' + qaqc_name+'/' + target_version + "_" + qaqc_name + "_"

# null
check_type = "null"
df_flagged = FAF_QAQC_01_null(df,check_array,outputfile_prefix,check_type)
FAF_QAQC_Summary([df_flagged],[dim_list],qaqc_name,dim_list,check_type)

# inf
check_type = "inf"
df_flagged = FAF_QAQC_01_inf(df,check_array,outputfile_prefix,check_type)
FAF_QAQC_Summary([df_flagged],[dim_list],qaqc_name,dim_list,check_type)


# =============================================================================
# check each attribute
# =============================================================================
outputfile_prefix = 'output/only_flagged/' + qaqc_name+'/' + qaqc_name + "_"
check_type = "attribute"
df_list_flagged = FAF_QAQC_01_attribute(df,grp_columns,outputfile_prefix)
grp_columns_list = [[x] for x in grp_columns]
dim_list = ["1" for x in grp_columns_list]
FAF_QAQC_Summary(df_list_flagged,grp_columns_list,qaqc_name,dim_list,check_type)
    