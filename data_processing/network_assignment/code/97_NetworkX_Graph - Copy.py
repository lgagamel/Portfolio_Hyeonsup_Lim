import pandas as pd
import networkx as nx
import pickle

# =============================================================================
# # Create a directed graph
# =============================================================================
# G = nx.DiGraph()
G = nx.Graph()


# =============================================================================
# add water
# =============================================================================
mode_prefix = "W"
links_df = pd.read_csv('output/01/water_links.csv')
links_df["Free_Speed"] = links_df["GEO_CLASS"].map({"I":8,"O":20,"G":8})
links_df["distance"] = links_df["distance"].round(3)
for _, row in links_df.iterrows():
    G.add_edge(row['node_A'], 
               row['node_B'],
               ID = row['link_id'],
               mode = mode_prefix,
               distance=row['distance'],
               distance=row['distance'],
               )
    
    

# =============================================================================
# add truck
# =============================================================================


# =============================================================================
# add port (connection between truck and water)
# =============================================================================

# Save graph to a pickle file
with open('output/03/G.pickle', 'wb') as f:
    pickle.dump(G, f)

