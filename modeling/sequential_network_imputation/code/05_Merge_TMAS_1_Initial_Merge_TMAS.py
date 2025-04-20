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
df_faf = pd.read_csv("output/step_3/FAF5_network_Simplified.csv")

# =============================================================================
# merge
# =============================================================================
gdf_faf = gdf_faf.merge(df_faf,on=['ID_S', 'BN_S', 'EN_S'],how='left')

# =============================================================================
# read tmas
# =============================================================================
# gdf_tmas = gpd.read_file(r"\\isilon-ops\NAOA\Projects\CMV-SAF\CMVRTC-DOCS\_CMVRTC_Project_Data\TMAS_CANNOT_BE_SHARED\01.Processed\00.STATION\shapefile\2018\2018.shp")
gdf_tmas = gpd.read_file(r"C:\Users\hslim\Dropbox\ORNL\21.Data\24.TMAS\99.Processed\00.STATION\shapefile\2021.shp")

# =============================================================================
# change crs
# =============================================================================
gdf_faf = gdf_faf.to_crs(crs="EPSG:3857")
gdf_tmas = gdf_tmas.to_crs(crs="EPSG:3857")


# =============================================================================
# dissolve tmas
# =============================================================================
gdf_tmas = gdf_tmas[['State_Code', 'Station_Id', 'Travel_Dir',"geometry"]]
gdf_tmas = gdf_tmas.dissolve(by=['State_Code', 'Station_Id', 'Travel_Dir'],as_index=False)
gdf_tmas["geometry"] = gdf_tmas["geometry"].centroid
ind = gdf_tmas["geometry"].apply(lambda p: np.isnan(p.x)|np.isinf(p.x)|np.isnan(p.y)|np.isinf(p.y))
gdf_tmas = gdf_tmas.loc[~ind]

# =============================================================================
# get nearest link for each tmas station
# =============================================================================
print("merge nearest links...")
# gpd.sjoin_nearest(gdf_tmas,gdf_faf,how="left")
gdf_out = gdf_tmas.sjoin_nearest(gdf_faf,how="left", max_distance=50)
gdf_out = gdf_out.drop(columns=["index_right"])


# =============================================================================
# output
# =============================================================================
gdf_out.to_file("output/step_5/TMAS2019_faf5.shp")
df_out = gdf_out[['State_Code', 'Station_Id', 'Travel_Dir', 'ID_S', 'BN_S','EN_S', 'DIR', 'Class', 'LENGTH', 'AB_17_All', 'TOT_17_All']]
df_out.to_csv("output/step_5/TMAS2019_faf5.csv",index=False)

# =============================================================================
# check1 with more than 1 link connected
# =============================================================================
# test_check1 = gdf_out.copy()
# test_check1["cnt"] = 1
# test_grp = test_check1.groupby(['State_Code', 'Station_Id', 'Travel_Dir'],as_index=False)["cnt"].sum()
# test_check1 = test_check1.drop(columns=["cnt"])
# test_check1 = test_check1.merge(test_grp,on=['State_Code', 'Station_Id', 'Travel_Dir'],how="left")
# test_check1 = test_check1.loc[test_check1["cnt"]>1]
# if len(test_check1)>0:
#     test_check1.to_file("output/step_5/check1.shp")


# =============================================================================
# check2 - not matched records
# =============================================================================
# test_check2 = gdf_out.copy()
# ind = test_check2["ID_S"].isnull()
# test_check2 = test_check2.loc[ind]
# if len(test_check2)>0:
#     test_check2.to_file("output/step_5/check2.shp")