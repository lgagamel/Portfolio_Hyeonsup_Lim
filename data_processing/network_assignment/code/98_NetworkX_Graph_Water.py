import pandas as pd
import networkx as nx
import pickle

# input parameters
mode_prefix = "W"
transfer_mode_prefix = "RO"

# =============================================================================
# # Load data from CSV files
# =============================================================================
nodes_df = pd.read_csv('output/01/water_nodes.csv',dtype=str)
links_df = pd.read_csv('output/01/water_links.csv',dtype=str)
RORO_nodes_df = pd.read_csv('output/01/water_RORO_nodes.csv',dtype=str)

# =============================================================================
# # Create a directed graph
# =============================================================================
G = nx.DiGraph()

# Add nodes from nodes_df
for node in nodes_df['ID']:
    G.add_node(node,
               mode = mode_prefix,
               )

# Add edges from links_df
for _, row in links_df.iterrows():
    G.add_edge(row['From ID'], 
               row['To ID'],
               ID = row['ID'],
               mode = mode_prefix,
               distance=float(row['distance']))
    
    G.add_edge(row['To ID'], 
               row['From ID'],
               ID = row['ID'],
               mode = mode_prefix,
               distance=float(row['distance']))

# Add nodes from RORO_nodes_df
for node in RORO_nodes_df['RO-RO_FAC_ID']:
    G.add_node(node,
               mode = transfer_mode_prefix,
               )

# Add edges from RORO_nodes_df
for _, row in RORO_nodes_df.iterrows():
    G.add_edge(row['RO-RO_FAC_ID'], 
               row['ID'],
               ID = row['RO-RO_FAC_ID'],
               mode = transfer_mode_prefix,
               distance=0)
    
    G.add_edge(row['ID'],
               row['RO-RO_FAC_ID'],               
               ID = row['RO-RO_FAC_ID'],
               mode = transfer_mode_prefix,
               distance=0)
    



# Save graph to a pickle file
with open('output/02/G_water.pickle', 'wb') as f:
    pickle.dump(G, f)

