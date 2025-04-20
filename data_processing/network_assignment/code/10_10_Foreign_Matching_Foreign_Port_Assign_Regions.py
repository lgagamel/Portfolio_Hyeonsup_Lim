import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

intput_folder = "output/10/10_9/"
output_folder = "output/10/10_10/"


# =============================================================================
# process Canada and Mexico from the previous step
# =============================================================================
region_list = [
    "801w",
    "801e",
    "801g",
    "802w",
    "802e",    
    ]

df_out = pd.DataFrame()
for region in region_list:
    gdf = gpd.read_file(intput_folder + region + ".shp")

    df = gdf[['CTRY_F', 'CTRY_F_NAM', 'FORPORT', 'FORPORT_NA','FAF_ZONE','TONNAGE']].copy()
    df = df.rename(columns={
        "CTRY_F_NAM":"CTRY_F_NAME",
        "FORPORT_NA":"FORPORT_NAME"
        })
    df["node_id_f"] = "F" + region
    df_out = pd.concat([df_out,df])

# =============================================================================
# process the rest of area
# =============================================================================
faf_mapping = pd.read_csv("../../__INPUT__/faf_foreign_zone_mapping.csv")
df = pd.read_csv("output/10/10_7/USACE_PORT_Foreign_to_FAF_Zone_803-808.csv")
df = df[['CTRY_F', 'CTRY_F_NAME', 'FORPORT', 'FORPORT_NAME','FAF_ZONE','TONNAGE']].copy()
df = df.merge(faf_mapping,on=["FAF_ZONE"],how="left")
df_out = pd.concat([df_out,df])


# =============================================================================
# groupby and output
# =============================================================================
df_out = df_out.groupby(['CTRY_F', 'CTRY_F_NAME', 'FORPORT', 'FORPORT_NAME','node_id_f'],as_index=False)['TONNAGE'].sum()
df_out.to_csv(output_folder + "USACE_PORT_Foreign_Match_Final.csv",index=False)

df_out["cnt"]=1
df_out = df_out.groupby(['CTRY_F', 'CTRY_F_NAME', 'FORPORT', 'FORPORT_NAME'],as_index=False)['cnt'].sum()
df_out.to_csv(output_folder + "check.csv",index=False) 
