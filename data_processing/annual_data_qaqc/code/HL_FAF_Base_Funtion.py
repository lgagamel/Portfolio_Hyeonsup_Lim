import pandas as pd

# =============================================================================
# user input
# =============================================================================
# FAF5_metadata_for_mapping_loc
FAF5_metadata_for_mapping_loc = "input/FAF5_metadata_for_mapping.xlsx"

# input_dtype
input_dtype = {'OOS':str,'fr_orig':str, 'dms_orig':str, 'dms_dest':str, 'dms_origst':str,
          'dms_destst':str, 'fr_dest':str, 'fr_inmode':str, 'dms_mode':str,
          'fr_outmode':str, 'sctg2':str, 'trade_type':str,
          'dist_band':str,'dist_band_text':str,'wgt_dist':float}
key_columns = ['fr_orig', 'dms_orig', 'dms_dest', 'fr_dest', 'fr_inmode','dms_mode', 'fr_outmode', 'sctg2', 'trade_type']

# base_year and target year list
year_list = ["2017","2018","2019","2020","2021","2022"]
base_year = "2017"

inputfile_loc_by_version = {    
    "FAF5.5":"https://www.dropbox.com/s/llsjd8898jq966b/FAF5.5_HiLoForecasts.csv?dl=1",
    "FAF5.5.1":r"C:\Users\9hl\Dropbox (Personal)\ORNL\19.ORNL_GitLab\02.Project\23\03_FAF\04_FAF5_Prelim\FAF5.5.1\05_TonMile_Update\output\FAF5.5.1_HiLoForecasts.csv",
    }

previous_version = "FAF5.5"
target_version = "FAF5.5.1"
measure_list = ["tons","value","current_value"]

# =============================================================================
# Sub-function to convert numeric code to description
# =============================================================================
def numeric2desc(df, col_list=[]):
    if len(col_list)==0:
        col_list = ['fr_orig','dms_orig','dms_dest','dms_origst','dms_destst','fr_dest','fr_inmode','dms_mode','fr_outmode','sctg2','trade_type']
    col_list = [col for col in col_list if (col in df.columns)]
    
    for col in col_list:
        df_mapping = pd.read_excel(FAF5_metadata_for_mapping_loc,sheet_name=col,dtype=input_dtype)
        df = df.merge(df_mapping,on=[col],how="left")
        df[col] = df[col] + "-" + df["_desc_"]
        df = df.drop(columns=["_desc_"])
        df[col] = df[col].fillna("")
    return df

# =============================================================================
# function to read FAF data
# =============================================================================
def read_FAF(version,base_year="2017",desc=True):
    print("read", version)
    inputfile_loc = inputfile_loc_by_version[version]
    df = pd.read_csv(inputfile_loc,dtype=input_dtype)
    df = df.fillna("")
    if desc:
        df = numeric2desc(df)
    
    # inter-intra
    df["intra_inter"] = "inter"
    ind = df["dms_orig"]==df["dms_dest"]
    df.loc[ind, "intra_inter"] = "intra"
    
    # add current_value_2017
    df["current_value_"+base_year] = df["value_"+base_year]
    
    return df