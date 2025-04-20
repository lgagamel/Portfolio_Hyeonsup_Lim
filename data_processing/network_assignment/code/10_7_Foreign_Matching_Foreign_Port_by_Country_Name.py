# =============================================================================
# Library
# =============================================================================
import pandas as pd
from fuzzywuzzy import process

output_folder = "output/10/10_7/"


# =============================================================================
# read data
# =============================================================================
df = pd.read_csv("output/10/10_2/USACE_PORT_Foreign.csv")
df_country_mapping = pd.read_csv("../../__INPUT__/Water/ORNL_Mapping/FAF5_Country_to_Foreign_Zone.csv")
# df_wpi = pd.read_csv("../../__INPUT__/Water/World_Port_Index/UpdatedPub150.csv")

df = df.groupby(["CTRY_F","CTRY_F_NAME",'FORPORT', 'FORPORT_NAME'],as_index=False)["TONNAGE"].sum()
df_country_mapping["FAF_ZONE"]=800+df_country_mapping["FAF_ZONE"]


# =============================================================================
# remove null port names
# =============================================================================
ind = df['CTRY_F_NAME'].isnull()
df = df.loc[~ind]

ind = df_country_mapping['FCNAME'].isnull()
df_country_mapping = df_country_mapping.loc[~ind]

# Function to map port names using fuzzy matching with similarity score and exact match flag
def map_port_name(port, reference_list):
    # Find the best match and its similarity score
    best_match, score = process.extractOne(port, reference_list)
    
    # Check if the match is exact
    exact_match = (port.lower() == best_match.lower())
    
    return best_match, score, exact_match



# =============================================================================
# filter for US ports
# =============================================================================
# Apply fuzzy matching
df[['mapped_port_name', 'similarity_score', 'exact_match']] = df['CTRY_F_NAME'].apply(
    lambda x: pd.Series(map_port_name(x, df_country_mapping['FCNAME'].tolist()))
)

# Merge df1 with df2 to get the port_id
df = df.merge(df_country_mapping[['FCNAME', 'FAF_ZONE']], left_on='mapped_port_name', right_on='FCNAME', how='left')

# # Drop the redundant 'port_name_y' column after merge
# df1.drop(columns=['port_name_y'], inplace=True)

# # Rename columns for clarity
# df1.rename(columns={'port_name_x': 'original_port_name', 'port_id': 'mapped_port_id'}, inplace=True)

# =============================================================================
# output
# =============================================================================
df.to_csv(output_folder+"USACE_PORT_Foreign_to_FAF_Zone.csv",index=False)

ind = df["FAF_ZONE"].isin([801,802])
df.loc[ind].to_csv(output_folder+"USACE_PORT_Foreign_to_FAF_Zone_801-802.csv",index=False)
df.loc[~ind].to_csv(output_folder+"USACE_PORT_Foreign_to_FAF_Zone_803-808.csv",index=False)
