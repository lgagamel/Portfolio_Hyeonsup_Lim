# =============================================================================
# Load Library
# =============================================================================
# import os
import networkx as nx
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import numpy as np
# from shapely.ops import nearest_points
# from shapely.geometry import Point, MultiPoint
# import time
# import fiona
# from shapely.geometry import shape

# =============================================================================
# Read Data
# =============================================================================
print("read data...")
gdf = gpd.read_file("output/step_1/FAF5_network_Savanah.shp", simplify=False)

gdf.explode()

# =============================================================================
# step1 - make node indices
# =============================================================================
print("make node indices...")
gdf["Begin_Node"] = gdf["geometry"].apply(lambda x: x.coords[0])
gdf["End_Node"] = gdf["geometry"].apply(lambda x: x.coords[-1])
gdf["ID"] = 0

gdf_b = gdf.groupby(["Begin_Node"],as_index=False)["ID"].sum()
gdf_e = gdf.groupby(["End_Node"],as_index=False)["ID"].sum()

gdf_b.columns = ["Pos","ID"]
gdf_e.columns = ["Pos","ID"]

df_node = gdf_b.append(gdf_e)
df_node = df_node.groupby(["Pos"],as_index=False)["ID"].sum()

df_node["ID"] = list(range(len(df_node)))
df_node = df_node[['ID','Pos']]

df_node['Longitude'] = df_node['Pos'].apply(lambda x: x[0])
df_node['Latitude'] = df_node['Pos'].apply(lambda x: x[1])

df_node.to_csv('output/step_2/node_list.csv',index=False)
df_node = df_node.set_index("Pos")

node_dict = dict(df_node["ID"])

# =============================================================================
# node to shapefile
# =============================================================================
df_node_shp = gpd.GeoDataFrame(df_node, geometry=gpd.points_from_xy(df_node["Longitude"], df_node["Latitude"]))
df_node_shp = df_node_shp.set_crs(gdf.crs)
df_node_shp.to_file("output/step_2/shapefile/Node.shp",index=False)
df_node_shp.drop(columns=["geometry"]).to_csv('output/step_2/shapefile/Node.csv',index=False)

# =============================================================================
# output 
# =============================================================================gdf[]
gdf["BN"] = gdf["Begin_Node"].apply(lambda x: node_dict[x])
gdf["EN"] = gdf["End_Node"].apply(lambda x: node_dict[x])
gdf[['OBJECTID','BN','EN']].to_csv('output/step_2/link_list.csv',index=False)


# =============================================================================
# calculate COST
# =============================================================================
# gdf_speed = gdf[["F_SYSTEM","SPEED_LIMI"]].copy()
# gdf_speed = gdf_speed.loc[gdf["SPEED_LIMI"]>0]
# gdf_speed = gdf_speed.groupby(["F_SYSTEM"],as_index=False)["SPEED_LIMI"].mean()
# gdf_speed = gdf_speed.rename(columns={"SPEED_LIMI":"AVG_SPEED"})
# gdf = gdf.merge(gdf_speed,on=["F_SYSTEM"],how="left")
# ind = gdf["SPEED_LIMI"]<=0
# gdf.loc[ind,"SPEED_LIMI"] = gdf.loc[ind,"AVG_SPEED"]
# gdf["COST"] = gdf["Length"]/gdf["SPEED_LIMI"]


# =============================================================================
# export to networkx edgelist
# =============================================================================
f = open("output/step_2/simplified_before.edgelist","w")
for i in range(len(gdf)):
    BN = str(gdf.iloc[i]["BN"])
    EN = str(gdf.iloc[i]["EN"])
    OBJECTID = str(gdf.iloc[i]["OBJECTID"])
    ID = str(gdf.iloc[i]["ID"])
    LENGTH = str(round(gdf.iloc[i]["LENGTH"],3))
    DIR = str(gdf.iloc[i]["DIR"])
    Class = str(gdf.iloc[i]["Class"])
    Speed_Limi = str(gdf.iloc[i]["Speed_Limi"])
    AB_17_All = str(round(gdf.iloc[i]["AB_17_All"],1))
    BA_17_All = str(round(gdf.iloc[i]["BA_17_All"],1))
    TOT_17_All = str(round(gdf.iloc[i]["TOT_17_All"],1))
    
    tmp_edge = str({"OBJECTID":OBJECTID,
                    "ID":ID,
                    "LENGTH":LENGTH,
                    "DIR":DIR,
                    "Class":Class,
                    "Speed_Limi":Speed_Limi,
                    "AB_17_All":AB_17_All,
                    "BA_17_All":BA_17_All,
                    "TOT_17_All":TOT_17_All})
    line = " ".join([BN,EN,tmp_edge])    
    f.write(line + "\n")
f.close()


# =============================================================================
# output gdf with only RouteID,ID,BN,EN
# =============================================================================
gdf = gdf[['OBJECTID','geometry']]
gdf.to_file("output/step_2/shapefile/FAF5_network_only_ID.shp",index=False)
