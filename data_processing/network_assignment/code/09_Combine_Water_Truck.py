import pandas as pd
import networkx as nx
import pickle
from itertools import combinations

# =============================================================================
# # Create a directed graph
# =============================================================================
# G = nx.DiGraph()
G = nx.Graph()
G_added = nx.Graph()

# =============================================================================
# add water
# =============================================================================
mode_prefix = "W"
links_df = pd.read_csv('output/01/water_links.csv')
links_df["speed"] = links_df["GEO_CLASS"].map({"I":8,"O":20,"G":8})
links_df["hour"] = links_df["distance"]/links_df["speed"]
links_df["link_type"] = mode_prefix + links_df["GEO_CLASS"]
links_df["vdf_ind"] = 0 
links_df["capacity"] = 999999999
for _, row in links_df.iterrows():
    G.add_edge(row['node_A'], 
               row['node_B'],
               link_id = row['link_id'],
               mode = mode_prefix,
               distance=row['distance'],
               hour = row["hour"],
               link_type = row["link_type"],
               vdf_ind = row["vdf_ind"],
               capacity = row["capacity"],
               )

# for testing only
nx.to_pandas_edgelist(G).to_csv("output/09/G_test_before.csv",index=False)

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
                    _vdf_ind_ = G.edges()[node,n1]["vdf_ind"]
                    _capacity_ = G.edges()[node,n1]["capacity"]
                    G.add_edge(n1, 
                               n1_new,
                               link_id = link_id1,
                               mode = mode_prefix,
                               distance=d1,
                               hour = h1,
                               link_type = lt1,
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
                               vdf_ind = _vdf_ind_,
                               capacity = _capacity_,
                               )
                G.remove_node(node)

# for testing only
nx.to_pandas_edgelist(G).to_csv("output/09/G_test_after.csv",index=False)
nx.to_pandas_edgelist(G_added).to_csv("output/09/G_test_added.csv",index=False)
print(total_changed_n)
    
# =============================================================================
# add truck centroid to port
# =============================================================================
mode_prefix = "T"
links_df = pd.read_csv("output/08/truck_port_to_centroid_skim_only_feasible.csv")
links_df["link_id"] = links_df["path"]
links_df["link_type"] = mode_prefix
links_df["vdf_ind"] = 0
links_df["capacity"] = 999999999

for _, row in links_df.iterrows():
    G.add_edge(row['node_id_t'], 
               row['node_id_p'],
               link_id = row['link_id'],
               mode = mode_prefix,
               distance=row['distance'],
               hour = row["hour"],
               link_type = row["link_type"],
               vdf_ind = row["vdf_ind"],
               capacity = row["capacity"],
               )
   

# =============================================================================
# add port to water (connection between truck and water)
# =============================================================================
mode_prefix = "P"
links_df = pd.read_csv("output/06/ports.csv")
# links_df["link_id"] = links_df["node_id_w"] +"-" +links_df["node_id_p"]
links_df["link_id"] = links_df["link_id_PW"]
links_df["distance"] = 0
links_df["hour"] = 0
links_df["link_type"] = mode_prefix
links_df["vdf_ind"] = 1 
links_df["capacity"] = links_df["TOTAL"]*2
for _, row in links_df.iterrows():
    G.add_edge(row['node_id_w'], 
               row['node_id_p'],
               link_id = row['link_id'],
               mode = mode_prefix,
               distance=row['distance'],
               hour = row["hour"],
               link_type = row["link_type"],
               vdf_ind = row["vdf_ind"],
               capacity = row["capacity"],
               )


# Save graph to a pickle file
with open('output/09/G.pickle', 'wb') as f:
    pickle.dump(G, f)

nx.to_pandas_edgelist(G).to_csv("output/09/G.csv",index=False)
