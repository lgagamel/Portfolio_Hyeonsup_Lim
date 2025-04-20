# =============================================================================
# Load Library
# =============================================================================
# import os
# import networkx as nx
# import geopandas as gpd
import pandas as pd
# from shapely.geometry import Point, MultiPoint
# from shapely.ops import nearest_points
import numpy as np
# from shapely.ops import nearest_points
# from shapely.geometry import Point, MultiPoint
# import time
# import fiona
# from shapely.geometry import shape
import plotly.express as px


# =============================================================================
# read data
# =============================================================================
df_network = pd.read_csv("output/step_7/simplified_network.csv")
df_faf_hpms = pd.read_csv("output/step_4/faf5_with_hpms_vol_two_direction.csv")
df_tmas = pd.read_csv('../01_TMAS_Data_Processing/output/1_volume_by_class_2021.csv')

# =============================================================================
# merge df_network and df_faf_hpms
# =============================================================================
df_network = df_network.merge(df_faf_hpms,on=['Node_O', 'Node_D'],how="left")

# =============================================================================
# drop TMAS data where volume is too small
# =============================================================================
all_class_columns = ["cls_" + str(col) for col in range(5,13+1)]
df_tmas["total_vol_check"] = df_tmas[all_class_columns].sum(axis=1)
ind = df_tmas["total_vol_check"]>100000
df_tmas = df_tmas.loc[ind]

# =============================================================================
# class volume to ratio
# =============================================================================
# for col in all_class_columns:
#     df_tmas[col] = df_tmas[col]/df_tmas["total_vol_check"]

# =============================================================================
# merge tmas
# =============================================================================
df_tmas = df_tmas[["TMAS","total_vol_check"]+all_class_columns]
df_network = df_network.merge(df_tmas,on=['TMAS'],how="left")




# =============================================================================
# mark original tmas data
# =============================================================================
df_network["TMAS_ind_original"]=0
ind = df_network["total_vol_check"]>0
df_network.loc[ind,"TMAS_ind_original"]=1


# =============================================================================
# make some TMAS null so that we can validate
# =============================================================================
def remove_tmas_direction(x):
    try:
        return "-".join(x.split("-")[:-1]) 
    except:
        return np.nan
    
df_network["TMAS_DIR_COMBINED"] = df_network["TMAS"].apply(lambda x: remove_tmas_direction(x))
TMAS_list = df_network["TMAS_DIR_COMBINED"].dropna().unique()

for random_seed in range(100):
    df_out = df_network.copy()
    np.random.seed(random_seed)
    df_out["TMAS_ind"]=df_out["TMAS_ind_original"]
    # ind = np.random.rand(len(df_out))<0.1
    TMAS_list_sub = TMAS_list[np.random.choice(len(TMAS_list), int(len(TMAS_list)*0.1))]
    ind = df_out["TMAS_DIR_COMBINED"].isin(TMAS_list_sub)
    df_out.loc[ind,"TMAS_ind"]=0
    ind_val =  (df_out["TMAS_ind_original"] == 1)&(df_out["TMAS_ind"] == 0)
    
    # =============================================================================
    # output
    # =============================================================================
    df_out.to_csv("output/step_8/"+str(random_seed)+".csv",index=False)
    
