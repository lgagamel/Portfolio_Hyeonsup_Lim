# =============================================================================
# Library
# =============================================================================
import pandas as pd

# custome by HL
import HL_FAF_Base_Funtion as hfb
import HL_Excel_Write as hew
from HL_FAF_QC_02_trend_over_years import FAF_QAQC_02
from HL_FAF_QC_Summary import FAF_QAQC_Summary

# =============================================================================
# user input
# =============================================================================
qaqc_name = "02_trend_over_years"
target_version = hfb.target_version

# measure list
measure_list = hfb.measure_list

# =============================================================================
# read data
# =============================================================================
year_list = hfb.year_list
df = hfb.read_FAF(hfb.target_version)

# =============================================================================
# Main Loop
# =============================================================================
thresholds_loc = "input/FAF5_QAQC_thresholds_" + qaqc_name + ".xlsx"
outputfile_prefix_all = 'output/all/' + qaqc_name+'/' + target_version + "_" + qaqc_name + "_" 
outputfile_prefix_flagged = 'output/only_flagged/'  + qaqc_name+'/' + target_version + "_" + qaqc_name + "_" 
for measure in measure_list:
    print(qaqc_name,measure)
    thresholds_by_grp_measure = pd.read_excel(thresholds_loc,sheet_name=measure)
    
    # outputfile loc
    outputfile_loc_all = outputfile_prefix_all + measure + ".xlsx"
    outputfile_loc_flagged = outputfile_prefix_flagged + measure + "_flagged.xlsx"
    
    # qa/qc
    grp_list, dim_list, df_list,df_list_flagged = FAF_QAQC_02(df,year_list,measure,thresholds_by_grp_measure)
    
    # wrtie output
    hew.write_excel(df_list,grp_list,outputfile_loc_all)
    hew.write_excel(df_list_flagged,grp_list,outputfile_loc_flagged)
    
    # write summary
    FAF_QAQC_Summary(df_list_flagged,grp_list,qaqc_name,dim_list,measure)
    


    