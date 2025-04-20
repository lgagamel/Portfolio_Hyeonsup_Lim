# =============================================================================
# Load Library
# =============================================================================
import os
import networkx as nx
import geopandas as gpd
import pandas as pd
from shapely.ops import nearest_points
from shapely.geometry import Point, MultiPoint
import time
import numpy as np
import pickle

import csv


# =============================================================================
# Read Data
# =============================================================================
# Example graphs
with open('output/02/G_water.pickle', 'rb') as f:
    G = pickle.load(f)


# for u, v in G.edges():    
#     G[u][v]['distance'] = G[u][v]['distance']**2 + G[u][v]['distance'] + 5
    
# Check the result
for u, v, data in G.edges(data=True):
    print(f"Edge ({u}, {v}) has distance: {data['distance']}")
    
centroid_df = pd.read_csv('output/01/water_RORO_nodes.csv',dtype=str)
centroid_list = list(centroid_df["RO-RO_FAC_ID"])

# =============================================================================
# output path
# =============================================================================
print(len(G.edges))
f_out = open("output/03/water_skim.csv", 'w')
# f_out.write("o,d,path,dist\n")
f_out.write("o,d,dist\n")
for i,o in enumerate(centroid_list):
    print(i,o)
    # dist_by_o,path_by_o = nx.single_source_dijkstra(G=G, source=o, weight='distance')
    # path_by_o = nx.single_source_dijkstra_path(G=G, source=o, weight='distance')
    dist_by_o = nx.single_source_dijkstra_path_length(G=G, source=o, weight='distance')    
    for d in list(centroid_list):
        try:
            # dist
            dist = dist_by_o[d]
            dist = str(round(dist,4))
            
            # # path
            # path_od = path_by_o[d]            
            # if len(path_od)>=2:
            #     for i in range(len(path_od)-1):
            #         e = (path_od[i],path_od[i+1])
            # path = "-".join(path_od)
            
            if len(dist)>0:
                # tmp_line = ",".join([o,d,path,dist]) + "\n"
                tmp_line = ",".join([o,d,dist]) + "\n"
                f_out.write(tmp_line)
            else:
                print(".",end="")
        except:
            pass
f_out.close()
