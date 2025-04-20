import pandas as pd

output_folder = "output/10/10_11/"

# =============================================================================
# read data
# =============================================================================
df_foreign = pd.read_csv("output/10/10_2/USACE_Foreign_Cargo_Combined.csv")
df_mapping_us_port = pd.read_csv("output/10/10_6/USACE_PORT_US_Match.csv")
df_mapping_foreign_port = pd.read_csv("output/10/10_10/USACE_PORT_Foreign_Match_Final.csv")


before_total = df_foreign["TONNAGE"].sum()

# =============================================================================
# merge
# =============================================================================
df_mapping_us_port = df_mapping_us_port[["STATE","PORT","PORT_NAME","node_id_p"]]
df_foreign = df_foreign.merge(df_mapping_us_port,on=["STATE","PORT","PORT_NAME"],how="left")

df_mapping_foreign_port = df_mapping_foreign_port[['CTRY_F', 'CTRY_F_NAME', 'FORPORT','FORPORT_NAME','node_id_f']]
df_foreign = df_foreign.merge(df_mapping_foreign_port,on=['CTRY_F', 'CTRY_F_NAME', 'FORPORT','FORPORT_NAME'],how="left")


# =============================================================================
# output
# =============================================================================
df_foreign.to_csv(output_folder+"Foreign_OD_check.csv",index=False)


# =============================================================================
# groupby
# =============================================================================
df_foreign = df_foreign.groupby(["Flow","node_id_p","node_id_f"],as_index=False)["TONNAGE"].sum()

# =============================================================================
# get OD of import and export
# =============================================================================
ind = df_foreign["Flow"]=="Import"
df_foreign_import = df_foreign.loc[ind].copy()

ind = df_foreign["Flow"]=="Export"
df_foreign_export = df_foreign.loc[ind].copy()

df_foreign_import = df_foreign_import.rename(columns={
    "node_id_f":"node_id_O",
    "node_id_p":"node_id_D"
    })

df_foreign_export = df_foreign_export.rename(columns={
    "node_id_p":"node_id_O",
    "node_id_f":"node_id_D",
    })

df_foreign_import = df_foreign_import[["Flow","node_id_O","node_id_D","TONNAGE"]]
df_foreign_export = df_foreign_export[["Flow","node_id_O","node_id_D","TONNAGE"]]
df_foreign = pd.concat([df_foreign_import,df_foreign_export])

after_total = df_foreign["TONNAGE"].sum()

# check
print(before_total,after_total,after_total-before_total)

# =============================================================================
# output
# =============================================================================
df_foreign = df_foreign.groupby(["Flow","node_id_O","node_id_D"],as_index=False)["TONNAGE"].sum()
ind = df_foreign["TONNAGE"]>0
df_foreign = df_foreign.loc[ind]
df_foreign.to_csv(output_folder+"Foreign_OD.csv",index=False)