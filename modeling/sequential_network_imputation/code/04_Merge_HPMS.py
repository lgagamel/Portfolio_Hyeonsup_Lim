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
# read faf
# =============================================================================
print("loading gdf...")
gdf_faf = gpd.read_file("output/step_3/shapefile/FAF5_network_Simplified.shp", simplify=False)
gdf_hpms = gpd.read_file(r'C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\30.HPMS\Highway_Performance_Monitoring_System_NHS.shp', simplify=False)



# =============================================================================
# conver hpms from line to point
# =============================================================================
gdf_hpms = gdf_hpms[['AADT', 'AADT_COMBI', 'AADT_SINGL','geometry']]
gdf_hpms = gdf_hpms.dropna()
gdf_hpms[['AADT', 'AADT_COMBI', 'AADT_SINGL']] = gdf_hpms[['AADT', 'AADT_COMBI', 'AADT_SINGL']].astype(int)
# gdf_hpms["geometry"] = gdf_hpms['geometry'].apply(lambda x: x.coords[0])
gdf_hpms["geometry"] = gdf_hpms["geometry"].centroid


# =============================================================================
# set crs
# =============================================================================
gdf_faf = gdf_faf.to_crs(crs="EPSG:3857")
gdf_hpms = gdf_hpms.to_crs(crs="EPSG:3857")


# =============================================================================
# get nearest link for each tmas station
# =============================================================================
print("merge nearest links...")
# gpd.sjoin_nearest(gdf_tmas,gdf_faf,how="left")
gdf_out = gdf_faf.sjoin_nearest(gdf_hpms,how="left", max_distance=50)
gdf_out = gdf_out.drop(columns=["index_right"])

# =============================================================================
# calculate mean where multiple hpms links are matched
# =============================================================================
df_out = gdf_out.groupby(['ID_S', 'BN_S', 'EN_S'],as_index=False)['AADT', 'AADT_COMBI', 'AADT_SINGL'].mean()

# =============================================================================
# output
# =============================================================================
df_out = df_out.dropna()
df_out = df_out.rename(columns={'AADT':'HPMS_ALL', 
                       'AADT_COMBI':'HPMS_COMBI', 
                       'AADT_SINGL':'HPMS_SINGL'})
df_out[['HPMS_ALL', 'HPMS_COMBI', 'HPMS_SINGL']] = df_out[['HPMS_ALL', 'HPMS_COMBI', 'HPMS_SINGL']].astype(int)
df_out.to_csv("output/step_4/faf5_with_hpms_vol.csv",index=False)

# =============================================================================
# make two-directional links
# =============================================================================
df_out = df_out.drop(columns=["ID_S"])
df_out1 = df_out.copy()
df_out2 = df_out.copy()
df_out1 = df_out1.rename(columns={"BN_S":"Node_O",
                                          "EN_S":"Node_D"})
df_out2 = df_out2.rename(columns={"BN_S":"Node_D",
                                          "EN_S":"Node_O"})

df_out = pd.concat([df_out1,df_out2])
df_out = df_out.drop_duplicates()
df_out.to_csv("output/step_4/faf5_with_hpms_vol_two_direction.csv",index=False)