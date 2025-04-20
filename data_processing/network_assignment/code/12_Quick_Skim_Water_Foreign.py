import pandas as pd
import networkx as nx
import pickle
from itertools import combinations
import numpy as np


output_folder = "output/12/"

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
links_df["link_p"] = (links_df["FUNC_CLASS"].isin(["N","S","U"]))*1
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
               )

# =============================================================================
# add foreign 
# =============================================================================
links_df = pd.read_csv('output/10/foreign_centroid_link.csv')
links_df["link_id"] = links_df["node_id_f"]
links_df["distance"]=0
links_df["hour"]=0
links_df["link_p"] = 0
links_df["link_type"]="WF"
links_df["vdf_ind"]=0
links_df["capacity"] = 999999999
for _, row in links_df.iterrows():
    G.add_edge(row['node_id'], 
               row['node_id_f'],
               link_id = row['link_id'],
               mode = mode_prefix,
               distance=row['distance'],
               hour = row["hour"],
               link_p = row["link_p"],
               link_type = row["link_type"],
               vdf_ind = row["vdf_ind"],
               capacity = row["capacity"],
               )



# =============================================================================
# add port
# =============================================================================
mode_prefix = "P"
links_df = pd.read_csv("output/06/ports.csv")
links_df["link_id"] = links_df["link_id_PW"]
links_df["distance"] = 0
links_df["hour"] = 0
links_df["link_p"] = 0
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
               link_p = row["link_p"],
               link_type = row["link_type"],
               vdf_ind = row["vdf_ind"],
               capacity = row["capacity"],
               )
                
# Save graph to a pickle file
with open(output_folder + 'G.pickle', 'wb') as f:
    pickle.dump(G, f)



# =============================================================================
# centroid & port
# =============================================================================
df_od = pd.read_csv('output/10/Foreign_OD.csv')
o_list = list(df_od["node_id_O"].unique())
d_list = list(df_od["node_id_D"].unique())
df_od = df_od.groupby(["node_id_O","node_id_D"])["TONNAGE"].sum()


# =============================================================================
# initiate volume
# =============================================================================
volume_by_link = {}
for u, v in G.edges():
    G[u][v]['volume'] = 0
    link_id = G[u][v]['link_id']        
    volume_by_link[link_id]=0
    
b5 = 1
b6 = 4

        
# =============================================================================
# output hour and distance
# =============================================================================
print(len(G.edges))
f_out = open(output_folder+"water_foreign_to_port_skim.csv", 'w')
f_out.write("node_id_O,node_id_D,hour,distance,path\n")
N = 100
for itr in range(N):
    # update C
    for u, v in G.edges():
        if G[u][v]['capacity']==0:
            G[u][v]['C'] = G[u][v]['hour']*G[u][v]['link_p']*100+\
                        G[u][v]['hour']*(1+b5*(100**b6))
        elif G[u][v]['capacity']>0:
            G[u][v]['C'] = G[u][v]['hour']*G[u][v]['link_p']*100+\
                        G[u][v]['hour']*(1+b5*(G[u][v]['volume']/G[u][v]['capacity'])**b6)
        else:
            raise("negative capacity")
                            
        if (np.isnan(G[u][v]['C']))|(np.isinf(G[u][v]['C'])):
            raise()
    for i,o in enumerate(o_list):
        print(itr,i,o)
        C_by_o,path_by_o = nx.single_source_dijkstra(G=G, source=o, weight='C')
        # path_by_o = nx.single_source_dijkstra_path(G=G, source=o, weight='hour')
        for j,d in enumerate(d_list):
            try:
                tons = df_od.loc[o,d]
            except:
                tons = 0
            tons = tons/N
            if tons>0:
                c = C_by_o[d]
                hour = 0
                distance = 0 
                path_od = path_by_o[d]
                path_join = []
                if len(path_od)>=2:
                    for i in range(len(path_od)-1):
                        e = (path_od[i],path_od[i+1])
                        distance = distance + G.edges[e]["distance"]
                        hour = hour + G.edges[e]["hour"]
                        path_join.append(G.edges[e]["link_id"])
                        G.edges[e]["volume"] = G.edges[e]["volume"] + tons
                hour = str(round(hour,4))
                distance = str(round(distance,4))
                path_join = "-".join(path_join)
                
                # link volume 
                if len(path_join)>0:
                    link_id_list = path_join.split("-")
                    for link_id in link_id_list:
                        if len(link_id)>0:
                            volume_by_link[link_id]=volume_by_link[link_id]+tons                        
                # try:
                #     hour = hour_by_o[d]         
                #     distance = 0 
                #     path_od = path_by_o[d]
                #     path_join = []
                #     if len(path_od)>=2:
                #         for i in range(len(path_od)-1):
                #             e = (path_od[i],path_od[i+1])
                #             distance = distance + G.edges[e]["distance"]
                #             path_join.append(G.edges[e]["link_id"])
                #     hour = str(round(hour,4))
                #     distance = str(round(distance,4))
                #     path_join = "-".join(path_join)
                    
                #     # link volume 
                #     if len(path_join)>0:
                #         link_id_list = path_join.split("-")
                #         for link_id in link_id_list:
                #             if len(link_id)>0:
                #                 volume_by_link[link_id]=volume_by_link[link_id]+tons                        
                # except:
                #     hour = ""
                #     distance = ""
                #     path_join = ""
                tmp_line = ",".join([str(itr),o,d,hour,distance,path_join]) + "\n"
                f_out.write(tmp_line)
f_out.close()

# write link volume output
df_link_volume = pd.DataFrame(list(volume_by_link.items()), columns=['link_id', 'tons'])
df_link_volume.to_csv(output_folder+"foreign_flow_link_volume.csv",index=False)
