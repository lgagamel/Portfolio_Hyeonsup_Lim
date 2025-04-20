# https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847

import osmnx as ox
import networkx as nx
import pandas as pd
import pickle
import os
import time
import numpy as np
import geopandas as gpd
import HL_Get_Simple_Graph as gsg
import HL_Get_Graph as gg
# =============================================================================
# read input center_point_list
# =============================================================================
# load pickle
with open('output/01/center_point_list.pkl', 'rb') as f:
    center_point_list = pickle.load(f)

with open('output/01/center_point_of_xy.pkl', 'rb') as f:
    center_point_of_xy = pickle.load(f)

# =============================================================================
# update_graph
# =============================================================================
def update_graph(center_point):
    outputloc = "../network/_network_original/" + str(center_point[0])+str(center_point[1])+".pkl"
    G, df_nodes = gg.Get_Graph(center_point)
    output = {"df_nodes":df_nodes,"G":G}
    with open(outputloc, 'wb') as f:
        pickle.dump(output, f)
    
    outputloc = "../network/_network_simple/" + str(center_point[0])+str(center_point[1])+".pkl"
    G, df_nodes = gsg.Get_Simple_Graph(center_point)
    output = {"df_nodes":df_nodes,"G":G}
    with open(outputloc, 'wb') as f:
        pickle.dump(output, f)
        
# =============================================================================
# Main Loop
# =============================================================================
G = []
start = time.time()
for i, center_point in enumerate(center_point_list):
    end = time.time()
    elapsed_time = end - start
    if elapsed_time>1000:
        raise("taking too long 2")
        
    # for testing
    # center_point = (29.620620966609575, -67.24861733232221)
    
    # check modified time
    outputloc = "../network/_network_original/" + str(center_point[0])+str(center_point[1])+".pkl"
    try: 
        modify_time = os.path.getmtime(outputloc)
        hours = (time.time()-modify_time)/3600
    except:
        hours = np.inf
    
    # only update if not updated for too long 
    if hours > 24*30*12:
        update_graph(center_point)
        print("updated",i,center_point)
    else:
        print("skipped",i,center_point)
    
    # load exisiting pickle
    if center_point in center_point_of_xy:
        outputloc = "../network/_network_original/" + str(center_point[0])+str(center_point[1])+".pkl"
    else:
        outputloc = "../network/_network_simple/" + str(center_point[0])+str(center_point[1])+".pkl"
    with open(outputloc, 'rb') as f:
        output = pickle.load(f)
    
    # combine G
    if len(output["G"])>0:
        if len(G) == 0:
            G = output["G"]
            df_nodes = output["df_nodes"]
        else:
            G = nx.compose(G,output["G"])
            df_nodes = pd.concat([df_nodes,output["df_nodes"]])
    
    # print("nodes",len(G.nodes))
    # print("edges",len(G.edges))

# =============================================================================
# output combined G
# =============================================================================
df_nodes = df_nodes.drop_duplicates()
output = {"df_nodes":df_nodes,"G":G}
with open("output/02/combined_network.pkl", 'wb') as f:
    pickle.dump(output, f)