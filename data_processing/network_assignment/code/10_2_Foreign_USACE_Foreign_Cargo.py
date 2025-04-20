# =============================================================================
# library
# =============================================================================
import pandas as pd
import csv
import HL_USACE_Base_Input

output_folder = "output/10/10_2/"

# =============================================================================
# Base Input
# =============================================================================
input_dtype = HL_USACE_Base_Input.input_dtype
inputfile_loc_by_year = HL_USACE_Base_Input.inputfile_loc_by_year
sheetname_import_by_year = HL_USACE_Base_Input.sheetname_import_by_year
sheetname_export_by_year = HL_USACE_Base_Input.sheetname_export_by_year
column_rename = HL_USACE_Base_Input.column_rename

# =============================================================================
# Main Loop
# =============================================================================
# year_list = range(2017,2021+1)
year_list = [2017]
for i, year in enumerate(year_list):
    print(i,year)
    inputfile_loc = inputfile_loc_by_year[year]
    sheetname_import = sheetname_import_by_year[year]
    sheetname_export = sheetname_export_by_year[year]
    df_import = pd.read_excel(inputfile_loc, sheet_name=sheetname_import,dtype=input_dtype)    
    df_export = pd.read_excel(inputfile_loc, sheet_name=sheetname_export,dtype=input_dtype)
    
    # column rename 
    df_import = df_import.rename(columns=column_rename)
    df_export = df_export.rename(columns=column_rename)
    
    # target columns
    target_columns = list(input_dtype)
    [target_columns.remove(col) for col in list(column_rename)]    
    df_import = df_import[target_columns]
    df_export = df_export[target_columns]
    
    # =============================================================================
    # output
    # =============================================================================
    if i==0:
        df_import.to_csv(output_folder+"USACE_Foreign_Cargo_Import.csv",index=False, quoting=csv.QUOTE_NONNUMERIC)
        df_export.to_csv(output_folder+"USACE_Foreign_Cargo_Export.csv",index=False, quoting=csv.QUOTE_NONNUMERIC)
    else:
        df_import.to_csv(output_folder+"USACE_Foreign_Cargo_Import.csv",index=False,mode="a",header=False, quoting=csv.QUOTE_NONNUMERIC)
        df_export.to_csv(output_folder+"USACE_Foreign_Cargo_Export.csv",index=False,mode="a",header=False, quoting=csv.QUOTE_NONNUMERIC)

# =============================================================================
# read data
# =============================================================================
df_import = pd.read_csv(output_folder+"USACE_Foreign_Cargo_Import.csv",dtype=input_dtype)   
df_export = pd.read_csv(output_folder+"USACE_Foreign_Cargo_Export.csv",dtype=input_dtype)
df_import = df_import.fillna("")
df_export = df_export.fillna("")

# =============================================================================
# combine two
# =============================================================================
df_import["Flow"] = "Import"
df_export["Flow"] = "Export"
df = pd.concat([df_import,df_export])

# =============================================================================
# adjustment for null PORT_NAME and FORPORT_NAME
# =============================================================================
ind = df["STATE"].isin(["PR","VI"])
df = df.loc[~ind]

total_t = df["TONNAGE"].sum()
ind1 = (df["PORT"].apply(lambda x: len(x)==0))|(df["PORT"].isnull())|(df["PORT_NAME"].apply(lambda x: len(x)==0))
ind2 = (df["CTRY_F"]=="9990")
ind = ind1|ind2
df["Unknown_Domestic"] = ind1
df["Unknown_Foreign"] = ind2
suppressed_t = df.loc[ind,"TONNAGE"].sum()
print("Unknown",suppressed_t/total_t)
df_grp = df.loc[ind].groupby(["Flow","STATE","PORT","PORT_NAME","CTRY_F","CTRY_F_NAME","FORPORT","FORPORT_NAME","Unknown_Domestic","Unknown_Foreign"],as_index=False)["TONNAGE"].sum()
df_grp.to_csv(output_folder+"USACE_Foreign_Cargo_Combined_Unknown.csv",index=False)

# drop unknown and adjust tonnage.
df = df.loc[~ind]
df["TONNAGE"] = df["TONNAGE"]*(total_t/df["TONNAGE"].sum())
print("Check after adjustment",sum(df["TONNAGE"])/total_t)

# =============================================================================
# output
# =============================================================================
df_grp = df.groupby(["Flow","STATE","PORT","PORT_NAME","CTRY_F","CTRY_F_NAME","FORPORT","FORPORT_NAME"],as_index=False)["TONNAGE"].sum()
df_grp.to_csv(output_folder+"USACE_Foreign_Cargo_Combined.csv",index=False)

df_grp = df.groupby(["STATE","PORT","PORT_NAME"],as_index=False)["TONNAGE"].sum()
df_grp.to_csv(output_folder+"USACE_PORT_US.csv",index=False)

df_grp = df.groupby(["CTRY_F","CTRY_F_NAME","FORPORT","FORPORT_NAME"],as_index=False)["TONNAGE"].sum()
df_grp.to_csv(output_folder+"USACE_PORT_Foreign.csv",index=False)
