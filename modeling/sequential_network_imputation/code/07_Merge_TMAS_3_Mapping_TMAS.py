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
# read data
# =============================================================================
df_network = pd.read_csv('output/step_3/FAF5_network_Simplified.csv')
df_hpms_to_tmas = pd.read_csv("output/step_6/TMAS2019_faf5.csv")

# =============================================================================
# make two-directional links
# =============================================================================
df_network = df_network.dropna()
df_network = df_network.drop(columns=["ID_S"])
df_network1 = df_network.copy()
df_network2 = df_network.copy()
df_network1 = df_network1.rename(columns={"BN_S":"Node_O",
                                          "EN_S":"Node_D"})
df_network2 = df_network2.rename(columns={"BN_S":"Node_D",
                                          "EN_S":"Node_O"})

df_network = pd.concat([df_network1,df_network2])
df_network = df_network.drop_duplicates()

# =============================================================================
# column for TMAS Station
# =============================================================================
df_hpms_to_tmas["State_Code"] = df_hpms_to_tmas["State_Code"].apply(lambda x: str(int(x)).zfill(2))
df_hpms_to_tmas["Travel_Dir"] = df_hpms_to_tmas["Travel_Dir"].astype(str)
df_hpms_to_tmas["TMAS"] = df_hpms_to_tmas["State_Code"] + "-" + df_hpms_to_tmas["Station_Id"] + "-" + df_hpms_to_tmas["Travel_Dir"]
df_hpms_to_tmas = df_hpms_to_tmas[['Node_O', 'Node_D', 'TMAS']]


# =============================================================================
# merge tmas by BN_S, EN_S
# =============================================================================
df_network = df_network.astype(int)
df_network = df_network.merge(df_hpms_to_tmas,on=['Node_O', 'Node_D'],how="left")

# =============================================================================
# output
# =============================================================================
df_network.to_csv("output/step_7/simplified_network.csv",index=False)