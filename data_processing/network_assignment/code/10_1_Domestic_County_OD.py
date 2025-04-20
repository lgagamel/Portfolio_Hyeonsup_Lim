import pandas as pd
import networkx as nx
import pickle
from itertools import combinations
import numpy as np
import os

output_folder = "output/10/10_1/"
# =============================================================================
# centroid data
# =============================================================================
centroid_df = pd.read_csv('output/01/Centroid.csv')
centroid_df["FIPS"] = centroid_df["FIPS"].apply(lambda x: str(int(x)).zfill(5))
FIPS_list = list(centroid_df["FIPS"].unique())

# =============================================================================
# FAF county OD
# =============================================================================
faf_df = pd.read_csv("https://www.dropbox.com/scl/fi/ogluxop3efhg5hz6wjqhl/FAF5.6.1.csv?rlkey=mylu4k2pk6l3mx78uufxvunbb&st=yfobfck3&dl=1")
grp_col = ['trade_type', 'dms_orig', 'dms_dest', 'sctg2', 'dms_mode']
faf_df = faf_df.groupby(grp_col,as_index=False)["tons_2017"].sum()
ind = faf_df["dms_mode"]==3
faf_df = faf_df.loc[ind]

print("faf",faf_df["tons_2017"].sum())


county_estimate_folder = r"C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\01.FAF\04.FAF5_County_Est\by_ODCM\county_update"
file_list = os.listdir(county_estimate_folder)
file_list = [f for f in file_list if f.split("_")[1][0]=="3"]
faf_county_df = pd.DataFrame()
for file in file_list:
    print(file)
    df_county = pd.read_csv(county_estimate_folder+"\\"+file)
    df_county = df_county[['trade_type', 'dms_orig', 'dms_dest', 'sctg2', 'dms_mode','dms_orig_cnty', 'dms_dest_cnty', 'f']]
    df_county = df_county.merge(faf_df,on=grp_col,how="left")
    df_county["tons_2017"] = df_county["tons_2017"]*df_county["f"]
    df_county = df_county.groupby(['dms_orig_cnty', 'dms_dest_cnty'],as_index=False)["tons_2017"].sum()
    faf_county_df = pd.concat([faf_county_df,df_county])
    faf_county_df = faf_county_df.groupby(['dms_orig_cnty', 'dms_dest_cnty'],as_index=False)["tons_2017"].sum()

# add ODM
df_county = pd.read_csv(r"C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\01.FAF\04.FAF5_County_Est\by_ODM\county\0_3.csv")
df_county["tons_2017"]=0.001
df_county = df_county.rename(columns={"county_o":"dms_orig_cnty","county_d":"dms_dest_cnty"})
df_county = df_county.groupby(['dms_orig_cnty', 'dms_dest_cnty'],as_index=False)["tons_2017"].sum()
faf_county_df = pd.concat([faf_county_df,df_county])
faf_county_df = faf_county_df.groupby(['dms_orig_cnty', 'dms_dest_cnty'],as_index=False)["tons_2017"].sum()


faf_county_df["FIPS_O"] = faf_county_df["dms_orig_cnty"].apply(lambda x: str(int(x)).zfill(5))
faf_county_df["FIPS_D"] = faf_county_df["dms_dest_cnty"].apply(lambda x: str(int(x)).zfill(5))
faf_county_df["ST_O"] = faf_county_df["FIPS_O"].apply(lambda x: x[:2])
faf_county_df["ST_D"] = faf_county_df["FIPS_D"].apply(lambda x: x[:2])
print("county",faf_county_df["tons_2017"].sum())
faf_county_df["total"] = faf_county_df["tons_2017"]*1000
faf_county_df = faf_county_df[["ST_O","ST_D","FIPS_O","FIPS_D","total"]]

for col in ["FIPS_O","FIPS_D"]:
    ind = faf_county_df[col].isin(FIPS_list)
    faf_county_df = faf_county_df.loc[ind]
print("after filtering",faf_county_df["total"].sum())
faf_county_df.to_csv(output_folder + "faf_county_od.csv",index=False)


# =============================================================================
# usace data
# =============================================================================
# usace_od_df = pd.read_excel('../../__INPUT__/Water/USACE_state_OD/pddb_state_orig_dest_2022.xlsx')
usace_od_df = pd.read_excel('../../__INPUT__/Water/USACE_state_OD/pddb_region_state_2017.xls', sheet_name='2017-state')
state_mapping = pd.read_csv("../../__INPUT__/state_mapping.csv")
print("usace state sum",usace_od_df["ShortTons"].sum())
state_mapping["st"] = state_mapping["st"].apply(lambda x: str(int(x)).zfill(2))
state_mapping["OrigCode"] = state_mapping["stusps"]
state_mapping["DestCode"] = state_mapping["stusps"]
state_mapping["ST_O"] = state_mapping["st"]
state_mapping["ST_D"] = state_mapping["st"]
usace_od_df = usace_od_df.merge(state_mapping[["OrigCode","ST_O"]],on=["OrigCode"],how="left")
usace_od_df = usace_od_df.merge(state_mapping[["DestCode","ST_D"]],on=["DestCode"],how="left")

ind = (usace_od_df["ST_O"].isnull())|(usace_od_df["ST_D"].isnull())
usace_od_df.loc[ind].to_csv(output_folder + "usace_state_od_dropped.csv",index=False)
usace_total = usace_od_df.loc[~ind,"ShortTons"].sum()
print(usace_od_df.loc[ind,"ShortTons"].sum()/usace_od_df["ShortTons"].sum())

usace_od_df = usace_od_df.rename(columns={"ShortTons":"usace_total"})
usace_od_df = usace_od_df.groupby(["ST_O","ST_D"],as_index=False)["usace_total"].sum()
usace_od_df.to_csv(output_folder + "usace_state_od.csv",index=False)
print("usace state sum",usace_od_df["usace_total"].sum())

# =============================================================================
# adjustment
# =============================================================================
faf_county_df_grp = faf_county_df.groupby(["ST_O","ST_D"],as_index=False)["total"].sum()
faf_county_df_grp = faf_county_df_grp.merge(usace_od_df,on=["ST_O","ST_D"],how="left")
faf_county_df_grp["adj_f"] = faf_county_df_grp["usace_total"]/faf_county_df_grp["total"]
faf_county_df_grp = faf_county_df_grp[["ST_O","ST_D","adj_f"]]

faf_county_df = faf_county_df.merge(faf_county_df_grp,on=["ST_O","ST_D"],how="left")
faf_county_df["total_adj"] = faf_county_df["total"]*faf_county_df["adj_f"]

print("total_adj sum",faf_county_df["total_adj"].sum())

# =============================================================================
# merge node id
# =============================================================================
centroid_df["FIPS_O"] = centroid_df["FIPS"]
centroid_df["FIPS_D"] = centroid_df["FIPS"]
centroid_df["node_id_O"] = centroid_df["node_id"]
centroid_df["node_id_D"] = centroid_df["node_id"]
faf_county_df = faf_county_df.merge(centroid_df[["FIPS_O","node_id_O"]],on=["FIPS_O"],how="left")
faf_county_df = faf_county_df.merge(centroid_df[["FIPS_D","node_id_D"]],on=["FIPS_D"],how="left")

faf_county_df["cnt"] = 1
faf_county_df_grp = faf_county_df.groupby(["FIPS_O","FIPS_D"],as_index=False)["cnt"].sum()
faf_county_df_grp = faf_county_df_grp.rename(columns={"cnt":"cnt_sum"})
faf_county_df = faf_county_df.merge(faf_county_df_grp,on=["FIPS_O","FIPS_D"],how="left")
faf_county_df["final"] = faf_county_df["total_adj"]/faf_county_df["cnt_sum"]

# =============================================================================
# drop intra county
# =============================================================================
ind = faf_county_df["FIPS_O"]==faf_county_df["FIPS_D"]
faf_county_df = faf_county_df.loc[~ind]

# =============================================================================
# final adjustment by national for domestic shipments
# =============================================================================
national_f = usace_total/faf_county_df["final"].sum()
print("national_f",national_f)
faf_county_df["final"] = faf_county_df["final"] * national_f
print("final check",usace_total,faf_county_df["final"].sum())

# =============================================================================
# output
# =============================================================================
faf_county_df.to_csv(output_folder + "county_od.csv",index=False)
print("final sum",faf_county_df["final"].sum())


