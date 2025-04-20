import numpy as np
import osmnx as ox
import networkx as nx
import pandas as pd

# =============================================================================
# Clean_G
# =============================================================================
def Clean_G(G):
    att_list = ["travel_time"]
    for x in G.edges:
        for att in list(G.edges[x]):
            if att not in att_list:
                del G.edges[x][att]

    att_list = ["x","y"]
    for x in G.nodes:
        for att in list(G.nodes[x]):
            if att not in att_list:
                del G.nodes[x][att]
    return G

# =============================================================================
# write df_nodes
# =============================================================================
def Write_df_nodes(G):
    df_nodes = []
    for ID,attribute_set in G.nodes(data=True):    
        x = attribute_set["x"]
        y = attribute_set["y"]
        df_nodes = df_nodes + [[ID,x,y]]
    df_nodes = pd.DataFrame(df_nodes, columns=["ID","x","y"])
    return df_nodes

# =============================================================================
# Get_Graph
# =============================================================================
def Get_Graph(center_point):
    # read osm network graph
    # G = ox.graph.graph_from_point(center_point, dist=55600, dist_type='bbox', network_type='drive',simplify=True,truncate_by_edge=True,retain_all=True)
    north = center_point[0] - 0.05
    south = center_point[0] + 0.05
    west = center_point[1] - 0.05
    east = center_point[1] + 0.05
    try:
        G = ox.graph.graph_from_bbox(north, south, east, west, network_type='drive', simplify=True, retain_all=False, truncate_by_edge=True)
    except:
        G = []
        df_nodes = []
        return G, df_nodes
    try:
        G = ox.add_edge_speeds(G)
    except:
        for x in G.edges:
            G.edges[x]["speed_kph"] = 82.9
    G = ox.add_edge_travel_times(G)
    df_nodes = Write_df_nodes(G)
    return G, df_nodes

# =============================================================================
# test
# =============================================================================
# center_point = (36.2, -84.4)
# G, df_nodes = Get_Graph(center_point)
# print(len(G.nodes),len(G.edges))



