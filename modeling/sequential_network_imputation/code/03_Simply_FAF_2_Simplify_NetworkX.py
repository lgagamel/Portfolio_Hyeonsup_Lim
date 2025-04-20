# =============================================================================
# Load Library
# =============================================================================
# import os
import networkx as nx
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import numpy as np
# from shapely.ops import nearest_points
# from shapely.geometry import Point, MultiPoint
# import time
# import fiona
# from shapely.geometry import shape


# =============================================================================
# load networkx edges
# =============================================================================
G = nx.read_edgelist("output/step_2/simplified_before.edgelist")

# =============================================================================
# columns_to_compare - this columns must be identical to be merged into one link from two
# =============================================================================
columns_to_compare = ["DIR",'Class', 'AB_17_All', 'TOT_17_All']

# =============================================================================
# check connected edges with only 2 neighbors
# =============================================================================
print("combine connected edgies with only 2 neighbors...")
nodes_to_remove = [n for n in G.nodes if len(list(G.neighbors(n))) == 2]

# =============================================================================
# add ID_LIST
# =============================================================================
print("add ID_LIST...")
for edge in G.edges:
    G.edges[edge]['ID_LIST'] = []

    
# =============================================================================
# Process to remove a node
# =============================================================================
i = 0 
nr = len(nodes_to_remove)
for node in nodes_to_remove:
    if len(list(G.neighbors(node))) == 2:
        i = i + 1
        print(i, nr)
        
        # initialize ID, COST, ID_LIST
        tmp_ID = np.inf
        tmp_LENGTH = 0
        tmp_ID_LIST = []
        
        # compare two edges if the attributes are same
        columns_to_compare_same = True
        for col in columns_to_compare:
            compare = []
            for neighbor in G.neighbors(node):
                compare = compare + [G.edges[(node,neighbor)][col]]
            if compare[0] != compare[1]:
                columns_to_compare_same = False
                break
        
        # if same, remove node and merge two edges
        if columns_to_compare_same:
            for neighbor in G.neighbors(node):
                tmp_DIR = G.edges[(node,neighbor)]['DIR']                
                tmp_Class = G.edges[(node,neighbor)]['Class']
                tmp_AB_17_All = G.edges[(node,neighbor)]['AB_17_All']
                tmp_TOT_17_All = G.edges[(node,neighbor)]['TOT_17_All']
                
                if int(G.edges[(node,neighbor)]['OBJECTID'])<tmp_ID:
                    tmp_ID = int(G.edges[(node,neighbor)]['OBJECTID'])
                tmp_LENGTH = tmp_LENGTH + float(G.edges[(node,neighbor)]['LENGTH'])
                if len(G.edges[(node,neighbor)]['ID_LIST']) > 0:
                    tmp_ID_LIST = tmp_ID_LIST + G.edges[(node,neighbor)]['ID_LIST']
                tmp_ID_LIST = tmp_ID_LIST + [int(G.edges[(node,neighbor)]['OBJECTID'])]
            # add new edge
            G.add_edge(*G.neighbors(node),
                       OBJECTID=tmp_ID,
                       DIR=tmp_DIR,
                       Class=tmp_Class,
                       LENGTH=tmp_LENGTH,
                       AB_17_All=tmp_AB_17_All,
                       TOT_17_All=tmp_TOT_17_All,
                       ID_LIST=tmp_ID_LIST)
            # delete the node
            G.remove_node(node)
nx.write_edgelist(G, "output/step_3/simplified_after.edgelist")

# =============================================================================
# add ID_LIST for links that are not merged (remain itself) and make unique ID_LIST
# =============================================================================
print("add ID_LIST for links that are not merged (remain itself)")
for i,edge in enumerate(G.edges):
    print(i)
    if len(G.edges[edge]['ID_LIST'])==0:
        G.edges[edge]['ID_LIST'] = [int(G.edges[edge]['OBJECTID'])]
    else:
        G.edges[edge]['ID_LIST'] = list(set(G.edges[edge]['ID_LIST']))
    
    

# =============================================================================
# Mapping Original Network's ID vs Simplified Network's ID
# =============================================================================
print("mapping...")
f = open('output/step_3/mapping_original_vs_simplified.csv','w')
f.write(','.join(['OBJECTID', 'ID_S', 'BN_S', 'EN_S'])+'\n')
for i,edge in enumerate(G.edges):
    print(i)
    ID_S = str(int(G.edges[edge]['OBJECTID']))
    BN_S = str(int(edge[0]))
    EN_S = str(int(edge[1]))
    
    OBJECTID_LIST = G.edges[edge]['ID_LIST']
    
    for OBJECTID in OBJECTID_LIST:
        f.write(','.join([str(int(OBJECTID)), ID_S, BN_S, EN_S])+'\n')
f.close()


# =============================================================================
# mapping_original_vs_simplified_final
# =============================================================================
df = pd.read_csv('output/step_3/mapping_original_vs_simplified.csv',dtype=int)
df['OBJECTID'] = df['OBJECTID'].astype(int)
df['cnt'] = 1
df = df.groupby(['OBJECTID', 'ID_S', 'BN_S', 'EN_S'],as_index=False)['cnt'].sum()
df.to_csv("output/step_3/mapping_original_vs_simplified_final.csv",index=False)




# =============================================================================
# Merge original shapefile with the mapping between original and simplified 
# =============================================================================

print("output gdf...")
gdf = gpd.read_file("output/step_2/shapefile/FAF5_network_only_ID.shp", simplify=False)
df_mapping_faf_nodes = pd.read_csv("output/step_2/link_list.csv")
gdf['OBJECTID'] = gdf['OBJECTID'].astype(int)
df_mapping_faf_nodes['OBJECTID'] = df_mapping_faf_nodes['OBJECTID'].astype(int)
gdf = gdf.merge(df_mapping_faf_nodes,on=['OBJECTID'],how='left')
gdf = gdf.merge(df,on=['OBJECTID'],how='left')
ind = gdf['ID_S'].isnull()
gdf = gdf.loc[~ind]
# gdf.loc[ind].to_file("output/step_3/shapefile/test.shp",index=False)
# gdf.loc[ind,'ID_S'] = gdf.loc[ind,'OBJECTID']
# gdf.loc[ind,'BN_S'] = gdf.loc[ind,'BN']
# gdf.loc[ind,'EN_S'] = gdf.loc[ind,'EN']


# mapping_original_vs_simplified_final
gdf['cnt'] = 1
df = gdf.groupby(['OBJECTID', 'ID_S', 'BN_S', 'EN_S'],as_index=False)['cnt'].sum()
df.to_csv("output/step_3/mapping_original_vs_simplified_final.csv",index=False)

# output shapefile
gdf = gdf[['ID_S', 'BN_S', 'EN_S','geometry']]
gdf[['ID_S', 'BN_S', 'EN_S']] = gdf[['ID_S', 'BN_S', 'EN_S']].astype(int)
gdf = gdf.dissolve(by=['ID_S', 'BN_S', 'EN_S'],as_index=False)
gdf.to_file("output/step_3/shapefile/FAF5_network_Simplified.shp",index=False)


# =============================================================================
# Final simplified network
# =============================================================================
for edge in G.edges:
    G.edges[edge]['ID_S'] = G.edges[edge]['OBJECTID']
    del G.edges[edge]['ID_LIST']
    del G.edges[edge]['OBJECTID']
    # del G.edges[edge]['F_SYSTEM']
nx.write_edgelist(G, "output/step_3/simplified_final.edgelist")



# =============================================================================
# output simplified.csv
# =============================================================================
print("output FAF5_network_Simplified.csv...")
f = open('output/step_3/FAF5_network_Simplified.csv','w')
f.write(','.join(['ID_S', 'BN_S', 'EN_S', 'DIR', 'Class', 'LENGTH','AB_17_All', 'TOT_17_All'])+'\n')
for i,edge in enumerate(G.edges):
    print(i)
    ID_S = str(int(G.edges[edge]['ID_S']))
    BN_S = str(int(edge[0]))
    EN_S = str(int(edge[1]))
    DIR = str(int(G.edges[edge]['DIR']))
    Class = str(int(G.edges[edge]['Class']))
    LENGTH = str(round(float(G.edges[edge]["LENGTH"]),3))
    AB_17_All = str(round(float(G.edges[edge]["AB_17_All"]),1))
    TOT_17_All = str(round(float(G.edges[edge]["TOT_17_All"]),1))
    f.write(','.join([ID_S, BN_S, EN_S, DIR, Class, LENGTH, AB_17_All, TOT_17_All])+'\n')
f.close()