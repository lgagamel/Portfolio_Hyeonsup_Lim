# =============================================================================
# Library
# =============================================================================
import pandas as pd
import HL_Excel_Write as hew

# =============================================================================
# user input
# =============================================================================
inputfile_loc = "output/summary.csv"
outputfile_loc = "output/summary.xlsx"

# =============================================================================
# read data
# =============================================================================
df_original = pd.read_csv(inputfile_loc)

# =============================================================================
# pivot table
# =============================================================================
df_list = []
grp_list = []
sheet_name_list = []
grp = ["check","dim","group"]

for check_type in df_original["check"].unique():
    df = df_original.copy()
    ind = df["check"]==check_type
    df = df.loc[ind]
    df = df.groupby(grp + ["measure"],as_index=False)["N_flag"].sum()
    df = df.pivot(index=grp,columns=["measure"],values="N_flag")
    df = df.reset_index()
    # df = df[["check","dim","group","tons","value","current_value","tmiles","v2w"]]
    df_list = df_list + [df]
    grp_list = grp_list + [grp]
    sheet_name_list = sheet_name_list + [check_type]

# =============================================================================
# output
# =============================================================================
hew.write_excel(df_list,grp_list,outputfile_loc,sheet_name_list)

