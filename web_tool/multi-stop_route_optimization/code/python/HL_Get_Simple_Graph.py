import numpy as np
import osmnx as ox
import networkx as nx
import pandas as pd


# =============================================================================
# Simplify_Graph
# =============================================================================
def Simplify_Graph(G):    
    # check connected edges with only 2 neighbors    
    nodes_to_remove = [n for n in G.nodes if len(list(G.neighbors(n))) == 2]
    
    # Process to remove a node    
    for node in nodes_to_remove:
        neighbor_list = list(G.neighbors(node))
        if len(neighbor_list) == 2:
            # add edge1
            travel_time = 0
            for neighbor in neighbor_list:                
                travel_time = travel_time + float(G.edges[(node,neighbor,0)]['travel_time'])
            G.add_edge(*neighbor_list,travel_time=travel_time)
            
            # add edge2
            neighbor_list.reverse()
            travel_time = 0
            for neighbor in neighbor_list:                
                travel_time = travel_time + float(G.edges[(node,neighbor,0)]['travel_time'])
            G.add_edge(*neighbor_list,travel_time=travel_time)
            
            # remove node
            G.remove_node(node)
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
# Get_Simple_Graph
# =============================================================================
def Get_Simple_Graph(center_point):
    north = center_point[0] - 0.05
    south = center_point[0] + 0.05
    west = center_point[1] - 0.05
    east = center_point[1] + 0.05
    
    # test for border node
    try:
        G_wo_outer_node = ox.graph.graph_from_bbox(north, south, east, west, network_type='drive', simplify=True, retain_all=False, truncate_by_edge=False)
        G = ox.graph.graph_from_bbox(north, south, east, west, network_type='drive', simplify=True, retain_all=False, truncate_by_edge=True)
    except:
        G = []
        df_nodes = []
        return G, df_nodes
    
    outer_border_node_list = []
    for x in G.nodes:
        try:
            G_wo_outer_node.nodes[x]
        except:
            outer_border_node_list = outer_border_node_list + [x]
    
    inner_border_node_list = []
    for border_node in outer_border_node_list:
        for border_edge in G.edges(border_node):
            tmp_inner_border_node_list = [e for e in list(border_edge) if e not in outer_border_node_list]
            for tmp_inner_border_node in tmp_inner_border_node_list:
                if tmp_inner_border_node not in inner_border_node_list:
                    inner_border_node_list = inner_border_node_list + tmp_inner_border_node_list
    
    try:
        G = ox.add_edge_speeds(G)
    except:
        for x in G.edges:
            G.edges[x]["speed_kph"] = 82.9
    G = ox.add_edge_travel_times(G)
    
    shortest_path_node_list = []
    inner_border_node_list = inner_border_node_list + outer_border_node_list
    for orig in inner_border_node_list:
        path = nx.single_source_dijkstra_path(G, orig, cutoff=None, weight='travel_time')    
        for dest in inner_border_node_list:
            if orig!=dest:
                try:
                    path_tmp = path[dest]
                    path_tmp = [n for n in path_tmp if n not in shortest_path_node_list]
                    shortest_path_node_list = shortest_path_node_list + path_tmp                
                except:
                    pass
    shortest_path_node_list = shortest_path_node_list + inner_border_node_list
    nodes_to_remove = [n for n in G.nodes if n not in shortest_path_node_list]
    print(len(G.nodes),len(G.edges))
    for node in nodes_to_remove:
        G.remove_node(node)
    print(len(G.nodes),len(G.edges))
    
    prev_n = len(G.nodes)
    for i in range(50):
        print(len(G.nodes),len(G.edges))
        G = Simplify_Graph(G)
        if prev_n == len(G.nodes):
            break
        prev_n = len(G.nodes)
    
    G = Clean_G(G)
    df_nodes = Write_df_nodes(G)
    return G, df_nodes




# =============================================================================
# test
# =============================================================================
# center_point = (36.2, -84.4)
# G, df_nodes = Get_Simple_Graph(center_point)
# print(len(G.nodes),len(G.edges))


    