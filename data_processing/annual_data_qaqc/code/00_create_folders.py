import os
import shutil


# =============================================================================
# remove existing output files
# =============================================================================
parent_folder = "output"
try:
    shutil.rmtree(parent_folder)
    os.mkdir(parent_folder)
except:
    pass

# =============================================================================
# output folders
# =============================================================================
folder_list = [
    parent_folder+"/all",
    parent_folder+"/only_flagged",
    # parent_folder+"/all/01_data_format_check",
    parent_folder+"/all/02_trend_over_years",
    parent_folder+"/all/03_changes_from_previous_version",
    parent_folder+"/all/04_v2w_over_years",
    parent_folder+"/all/05_change_of_shares",
    parent_folder+"/only_flagged/01_data_format_check",
    parent_folder+"/only_flagged/02_trend_over_years",
    parent_folder+"/only_flagged/03_changes_from_previous_version",
    parent_folder+"/only_flagged/04_v2w_over_years",
    parent_folder+"/only_flagged/05_change_of_shares",]

# =============================================================================
# create folders
# =============================================================================
for folder in folder_list:
    try:
        os.mkdir(folder)
    except:
        pass
    
