# =============================================================================
# Library
# =============================================================================
import pandas as pd
import geopandas as gpd
from fuzzywuzzy import process

input_folder = "output/10/10_3/"
output_folder = "output/10/10_4/"

# =============================================================================
# read data
# =============================================================================
df = pd.read_csv(input_folder+"USACE_PORT_US_Match_by_ID.csv")
principal_port_nodes_gdf = gpd.read_file('output/06/ports.shp')


# =============================================================================
# principal_port_nodes_gdf name
# =============================================================================
principal_port_nodes_gdf["PORT_NAMEP"] = principal_port_nodes_gdf["PORT_NAME"]
ind = principal_port_nodes_gdf['PORT_NAMEP'].isnull()
principal_port_nodes_gdf.loc[ind,'PORT_NAMEP'] = principal_port_nodes_gdf.loc[ind,'RORO_NAME']
principal_port_nodes_gdf = principal_port_nodes_gdf[['PORT', 'PORT_NAMEP','node_id_p']]

# =============================================================================
# remove null port names
# =============================================================================
ind = df['PORT_NAMEP'].isnull()
df_good = df.loc[~ind].copy()
df_good.to_csv(output_folder + "USACE_PORT_US_Match_by_ID.csv",index=False)

df_bad = df.loc[ind].copy()


ind = principal_port_nodes_gdf['PORT_NAMEP'].isnull()
principal_port_nodes_gdf = principal_port_nodes_gdf.loc[~ind]
principal_port_nodes_gdf['PORT_NAMEP_a'] = principal_port_nodes_gdf['PORT_NAMEP']

# Function to map port names using fuzzy matching with similarity score and exact match flag
def map_port_name(port, reference_list):
    # Find the best match and its similarity score
    best_match, score = process.extractOne(port, reference_list)
    
    # Check if the match is exact
    exact_match = (port.lower() == best_match.lower())
    
    return best_match, score, exact_match



# Apply fuzzy matching
df_bad[['mapped_port_name', 'similarity_score', 'exact_match']] = df_bad['PORT_NAME'].apply(
    lambda x: pd.Series(map_port_name(x, principal_port_nodes_gdf['PORT_NAMEP_a'].tolist()))
)

# Merge df1 with df2 to get the port_id
df_bad = df_bad.drop(columns=['PORT', 'PORT_NAMEP','node_id_p'])
df_bad = df_bad.merge(principal_port_nodes_gdf[['PORT_NAMEP_a','PORT', 'PORT_NAMEP','node_id_p']], left_on='mapped_port_name', right_on='PORT_NAMEP_a', how='left')
df_bad.to_csv(output_folder + "USACE_PORT_US_Match_by_Name.csv",index=False)
