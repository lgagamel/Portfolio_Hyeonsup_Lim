# =============================================================================
# Library
# =============================================================================
import pandas as pd

# custome by HL
import HL_FAF_Base_Funtion as hfb
import HL_Excel_Write as hew
from HL_FAF_QC_03_changes_from_previous_version import FAF_QAQC_03
from HL_FAF_QC_Summary import FAF_QAQC_Summary

# =============================================================================
# user input
# =============================================================================
qaqc_name = "03_changes_from_previous_version"

# input/output
ver1 = hfb.previous_version
ver2 = hfb.target_version

# measure list
measure_list = hfb.measure_list

# =============================================================================
# read data
# =============================================================================
year_list = hfb.year_list
df1 = hfb.read_FAF(ver1)
df2 = hfb.read_FAF(ver2)
df1["current_value_2017"] = df1["value_2017"]
df2["current_value_2017"] = df2["value_2017"]

raise()
# =============================================================================
# Main Loop
# =============================================================================
thresholds_loc = "input/FAF5_QAQC_thresholds_" + qaqc_name + ".xlsx"
# outputfile_prefix_all = 'output/all/'  + qaqc_name+'/' + ver1 + "_vs_" + ver2 + "_" + qaqc_name + "_" 
# outputfile_prefix_flagged = 'output/only_flagged/' + qaqc_name+'/' + ver1 + "_vs_" + ver2 +  "_" + qaqc_name + "_" 
outputfile_prefix_all = 'output/all/'  + qaqc_name+'/'
outputfile_prefix_flagged = 'output/only_flagged/' + qaqc_name + "/" 
for measure in measure_list:
    print(qaqc_name,measure)
    thresholds_by_grp_measure = pd.read_excel(thresholds_loc,sheet_name=measure)
    
    # outputfile loc
    outputfile_loc_all = outputfile_prefix_all + measure + ".xlsx"
    outputfile_loc_flagged = outputfile_prefix_flagged + measure + "_flagged.xlsx"
    
    # qa/qc
    grp_list, dim_list, df_list,df_list_flagged = FAF_QAQC_03(df1,df2,ver1,ver2,year_list,measure,thresholds_by_grp_measure)
    
    # wrtie output
    hew.write_excel(df_list,grp_list,outputfile_loc_all)
    hew.write_excel(df_list_flagged,grp_list,outputfile_loc_flagged)
    
    # write summary
    FAF_QAQC_Summary(df_list_flagged,grp_list,qaqc_name,dim_list,measure)


# outputfile_loc_flagged_copy = 'output/only_flagged/03_changes_from_previous_version/test.xlsx'
# hew.write_excel(df_list_flagged,grp_list,outputfile_loc_flagged_copy)