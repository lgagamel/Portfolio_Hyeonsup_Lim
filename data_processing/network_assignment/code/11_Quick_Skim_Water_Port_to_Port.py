import pandas as pd
import networkx as nx
import pickle
from itertools import combinations
import numpy as np

output_folder = "output/11/"

# =============================================================================
# # Create a directed graph
# =============================================================================
# G = nx.DiGraph()
G = nx.Graph()
G_added = nx.Graph()

# =============================================================================
# add water
# =============================================================================
# Laura@BTS: for waterway network func_class=N (non navigable) = S-shallow draft or U-special vessel; depth less than 9 feet

mode_prefix = "W"
links_df = pd.read_csv('output/01/water_links.csv')
links_df["speed"] = links_df["GEO_CLASS"].map({"I":8,"O":20,"G":8})
links_df["hour"] = links_df["distance"]/links_df["speed"]
# links_df["link_p"] = (links_df["FUNC_CLASS"].isin(["N","S","U"]))*1
links_df["link_p"] = (links_df["FUNC_CLASS"].isin(["N","U"]))*1
links_df["link_type"] = mode_prefix + links_df["GEO_CLASS"]
links_df["vdf_ind"] = 0 
links_df["capacity"] = links_df["TOTALUP"]+links_df["TOTALDOWN"]
links_df["capacity"] = links_df["capacity"].fillna(0)

for _, row in links_df.iterrows():
    G.add_edge(row['node_A'], 
               row['node_B'],
               link_id = row['link_id'],
               mode = mode_prefix,
               distance=row['distance'],
               hour = row["hour"],
               link_p = row["link_p"],
               link_type = row["link_type"],
               vdf_ind = row["vdf_ind"],
               capacity = row["capacity"],
               volume = 0,
               )

# for testing only
nx.to_pandas_edgelist(G).to_csv(output_folder+"G_test_before.csv",index=False)

# =============================================================================
# add link where the link type changes
# =============================================================================
ports_df = pd.read_csv("output/06/ports.csv")
ports_node_id_w = list(ports_df["node_id_w"])
node_list = list(G.nodes)
total_changed_n = 0 
for node in node_list:
    if node not in ports_node_id_w:
        n = G.degree(node)
        if n>=2:
            neighbor_node = list(G.neighbors(node))
            neighbor_node_comb = list(combinations(neighbor_node, 2))
            
            change_ind = False
            for two_nodes in neighbor_node_comb:
                n1 = two_nodes[0]
                n2 = two_nodes[1]
                lt1 = G.edges()[node,n1]["link_type"]
                lt2 = G.edges()[node,n2]["link_type"]
                
                if (lt1!="CHG")&(lt2!="CHG")&(lt1!=lt2)&((lt1=="WO")|(lt2=="WO")):
                    change_ind = True
            
            if change_ind:
                total_changed_n = total_changed_n + 1
                for n1 in neighbor_node:
                    n1_new = n1 + "-" + node                    
                    lt1 = G.edges()[node,n1]["link_type"]
                    link_id1 = G.edges()[node,n1]["link_id"]                    
                    d1 = G.edges()[node,n1]["distance"]
                    h1 = G.edges()[node,n1]["hour"]
                    _lp_ = G.edges()[node,n1]["link_p"]
                    _vdf_ind_ = G.edges()[node,n1]["vdf_ind"]
                    _capacity_ = G.edges()[node,n1]["capacity"]
                    G.add_edge(n1, 
                               n1_new,
                               link_id = link_id1,
                               mode = mode_prefix,
                               distance=d1,
                               hour = h1,                               
                               link_type = lt1,
                               link_p = _lp_,
                               vdf_ind = _vdf_ind_,
                               capacity = _capacity_,
                               )
                
                for two_nodes in neighbor_node_comb:
                    n1 = two_nodes[0]
                    n2 = two_nodes[1]
                    n1_new = n1 + "-" + node
                    n2_new = n2 + "-" + node
                    lt1 = G.edges()[node,n1]["link_type"]
                    lt2 = G.edges()[node,n2]["link_type"]
                    # link_id1 = G.edges()[node,n1]["link_id"]
                    # link_id2 = G.edges()[node,n2]["link_id"]                    
                    # d1 = G.edges()[node,n1]["distance"]
                    # d2 = G.edges()[node,n2]["distance"]
                    # h1 = G.edges()[node,n1]["hour"]
                    # h2 = G.edges()[node,n2]["hour"]
                    _lp_ = G.edges()[node,n1]["link_p"]
                    _vdf_ind_ = G.edges()[node,n1]["vdf_ind"]
                    _capacity_ = G.edges()[node,n1]["capacity"]
                    if (lt1!="CHG")&(lt2!="CHG")&(lt1!=lt2)&((lt1=="WO")|(lt2=="WO")):
                        _link_type_ = "CHG"
                    else:
                        _link_type_ = "X"
                            
                    G.add_edge(n1_new, 
                               n2_new,
                               link_id = "X",
                               mode = mode_prefix,
                               distance=0,
                               hour = 0,
                               link_type = _link_type_,
                               link_p = _lp_,
                               vdf_ind = _vdf_ind_,
                               capacity = _capacity_,
                               )
                    
                    # for testing only
                    G_added.add_edge(n1_new, 
                               n2_new,
                               link_id = "X",
                               mode = mode_prefix,
                               distance=0,
                               hour = 0,
                               link_type = _link_type_,
                               link_p = _lp_,
                               vdf_ind = _vdf_ind_,
                               capacity = _capacity_,
                               )
                G.remove_node(node)
                
# Save graph to a pickle file
with open(output_folder + 'G_water.pickle', 'wb') as f:
    pickle.dump(G, f)



# # update volume
# for u, v in G.edges():    
#     G[u][v]['volume'] = 0
        


# # update C
# b3 = 100
# for u, v in G.edges():    
#     G[u][v]['C'] = G[u][v]['hour']+\
#                    b3*(G[u][v]['link_type']=="CHG")
#     if (np.isnan(G[u][v]['C']))|(np.isinf(G[u][v]['C'])):
#         raise()
        

# # =============================================================================
# # centroid & port
# # =============================================================================
# port_df = pd.read_csv('output/06/ports.csv')
# node_id_w_list = list(port_df["node_id_w"])
# node_id_p_list = list(port_df["node_id_p"])

# # =============================================================================
# # output hour and distance
# # =============================================================================
# print(len(G.edges))
# f_out = open(output_folder+"water_port_to_port_skim.csv", 'w')
# # f_out.write("o,d,path,dist\n")
# f_out.write("node_id_p_o,node_id_w_o,node_id_p_d,node_id_w_d,hour,distance,path\n")
# for i,o in enumerate(node_id_w_list):
#     node_id_w_o = o
#     node_id_p_o = node_id_p_list[i]    
#     hour_by_o,path_by_o = nx.single_source_dijkstra(G=G, source=o, weight='C')
#     # path_by_o = nx.single_source_dijkstra_path(G=G, source=o, weight='hour')
#     for j,d in enumerate(node_id_w_list):
#         if o!=d:
#             node_id_w_d = d
#             node_id_p_d = node_id_p_list[j]
#             print("O",i,o,node_id_p_o)
#             print("D",j,d,node_id_p_d)            
#             try:
#                 hour = hour_by_o[d]         
#                 distance = 0 
#                 path_od = path_by_o[d]
#                 path_join = []
#                 if len(path_od)>=2:
#                     for i in range(len(path_od)-1):
#                         e = (path_od[i],path_od[i+1])
#                         distance = distance + G.edges[e]["distance"]
#                         # G.edges[e]["volume"] = G.edges[e]["volume"] + tons
#                         path_join.append(G.edges[e]["link_id"])
#                 hour = str(round(hour,4))
#                 distance = str(round(distance,4))
#                 path_join = "-".join(path_join)
#             except:
#                 hour = ""
#                 distance = ""
#                 path_join = ""
#             tmp_line = ",".join([node_id_p_o,node_id_w_o,node_id_p_d,node_id_w_d,hour,distance,path_join]) + "\n"
#             f_out.write(tmp_line)
# f_out.close()