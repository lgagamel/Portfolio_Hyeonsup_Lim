import pandas as pd
import networkx as nx
import pickle
import pandas as np


# =============================================================================
# # Create a directed graph
# =============================================================================
# G = nx.DiGraph()
G = nx.Graph()


# =============================================================================
# truck_links
# =============================================================================
mode_prefix = "T"
links_df = pd.read_csv('output/01/truck_links.csv')

# speed adjustment
speed_r = (links_df["AB_FINALSP"]/links_df["SPEED_LIMI"]).mean()
links_df["speed"] = links_df["AB_FINALSP"]
ind = links_df["speed"].isnull()
links_df.loc[ind,"speed"] = links_df.loc[ind,"SPEED_LIMI"]*speed_r

# hour calculation
links_df["hour"] = links_df["distance"]/links_df["speed"]

for _, row in links_df.iterrows():
    G.add_edge(row['node_A'], 
                row['node_B'],
                link_id = row['link_id'],
                mode = mode_prefix,
                distance=row['distance'],
                hour=row['hour'],
                )

# Save graph to a pickle file
with open('output/03/G.pickle', 'wb') as f:
    pickle.dump(G, f)



# =============================================================================
# centroid & port
# =============================================================================
centroid_df = pd.read_csv('output/01/Centroid.csv')
port_df = pd.read_csv('output/02/ports.csv')
o_list = list(port_df["node_id_t"])
node_id_p_list = list(port_df["node_id_p"])
d_list = list(centroid_df["node_id"])

# =============================================================================
# output hour and distance
# =============================================================================
print(len(G.edges))
f_out = open("output/03/truck_port_to_centroid_skim.csv", 'w')
# f_out.write("o,d,path,dist\n")
f_out.write("node_id_p,node_id_t,hour,distance,path\n")
for i,o in enumerate(o_list):
    node_id_p = node_id_p_list[i]
    print(i,o,node_id_p)
    hour_by_o,path_by_o = nx.single_source_dijkstra(G=G, source=o, weight='hour')
    # path_by_o = nx.single_source_dijkstra_path(G=G, source=o, weight='hour')
    for d in list(d_list):
        node_id_t = d
        try:
            hour = hour_by_o[d]            
            distance = 0 
            path_od = path_by_o[d]
            path_join = []
            if len(path_od)>=2:
                for i in range(len(path_od)-1):
                    e = (path_od[i],path_od[i+1])
                    distance = distance + G.edges[e]["distance"]
                    path_join.append(G.edges[e]["link_id"])
            hour = str(round(hour,4))
            distance = str(round(distance,4))
            path_join = "-".join(path_join)
        except:
            hour = ""
            distance = ""
            path_join = ""
        tmp_line = ",".join([node_id_p,node_id_t,hour,distance,path_join]) + "\n"
        f_out.write(tmp_line)
f_out.close()