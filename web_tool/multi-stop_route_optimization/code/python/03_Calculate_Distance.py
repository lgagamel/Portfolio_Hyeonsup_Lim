# https://stackoverflow.com/questions/62262640/how-can-i-get-a-shortest-path-on-openstreetmap
import networkx as nx
import pickle
import numpy as np
import pandas as pd
import time

# =============================================================================
# load input
# =============================================================================
df_xy = pd.read_csv("output/01/xy.csv")
df_xy = df_xy.dropna()

# get a graph
with open("output/02/combined_network.pkl", 'rb') as f:
    output = pickle.load(f)

G = output["G"]
df_nodes = output["df_nodes"]


# =============================================================================
# get node_list from input_list
# =============================================================================
node_list = []
for i in range(len(df_xy)):
    x = df_xy.iloc[i]["x"]
    y = df_xy.iloc[i]["y"]
    ind = np.argmin((df_nodes["x"]-x)**2+(df_nodes["y"]-y)**2)
    node = int(df_nodes.iloc[ind]["ID"])
    node_list = node_list + [node]



# =============================================================================
# Main Loop
# =============================================================================
dist_array = np.empty((len(node_list),len(node_list)))
dist_array[:] = np.nan
start = time.time()
for i, orig in enumerate(node_list):
    end = time.time()
    elapsed_time = end - start
    if elapsed_time>1000:
        raise("taking too long 3")
    length = nx.single_source_dijkstra_path_length(G, orig, cutoff=None, weight='travel_time')
    for j, dest in enumerate(node_list):
        try:
            dist_array[i,j] = length[dest]
        except:
            pass

# =============================================================================
# update based on simple distance
# =============================================================================
df_gcd = pd.read_csv("output/01/xy_gcd.csv")
ind = df_gcd.simple_dist.isnull()
df_gcd = df_gcd.loc[~ind]
for i in range(len(df_gcd)):
    o_i = int(df_gcd.iloc[i]["o_i"])
    d_i = int(df_gcd.iloc[i]["d_i"])
    simple_dist = df_gcd.iloc[i]["simple_dist"]
    dist_array[o_i,d_i] = simple_dist
    
# dist_array = np.nan_to_num(dist_array, nan=99999999, posinf=99999999, neginf=99999999)    
                
            


# =============================================================================
# output    
# =============================================================================
with open("output/03/node_list.pkl", 'wb') as f:
    pickle.dump(node_list, f)
    
with open("output/03/dist_array.pkl", 'wb') as f:
    pickle.dump(dist_array, f)
    