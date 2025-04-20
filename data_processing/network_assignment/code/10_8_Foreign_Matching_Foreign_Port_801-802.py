# =============================================================================
# Library
# =============================================================================
import pandas as pd
from fuzzywuzzy import process

output_folder = "output/10/10_8/"

# =============================================================================
# read data
# =============================================================================
df = pd.read_csv("output/10/10_7/USACE_PORT_Foreign_to_FAF_Zone_801-802.csv")
df_foreign_port = pd.read_excel("../../__INPUT__/Water/USACE_from_Marin_Port_GeoCode/ForeignPortsGeocoded_2016-06-28_for BTSFAF.xlsx")

# =============================================================================
# remove null port names
# =============================================================================
ind = df['FORPORT_NAME'].isnull()
df = df.loc[~ind]

ind = df_foreign_port['Foreign_Port_Name'].isnull()
df_foreign_port = df_foreign_port.loc[~ind]


df["FORPORT_NAME_a"] = df["FORPORT_NAME"]+","+df["CTRY_F_NAME"]
df_foreign_port["Foreign_Port_Name_a"] = df_foreign_port["Foreign_Port_Name"]+", "+df_foreign_port["Common_Country_Name"]

# Function to map port names using fuzzy matching with similarity score and exact match flag
def map_port_name(port, reference_list):
    # Find the best match and its similarity score
    best_match, score = process.extractOne(port, reference_list)
    
    # Check if the match is exact
    exact_match = (port.lower() == best_match.lower())
    
    return best_match, score, exact_match




# check unique Main Port Name
print(len(df_foreign_port),len(df_foreign_port["Foreign_Port_Name_a"].unique()))

# Apply fuzzy matching
df[['mapped_port_name', 'similarity_score', 'exact_match']] = df['FORPORT_NAME_a'].apply(
    lambda x: pd.Series(map_port_name(x, df_foreign_port['Foreign_Port_Name_a'].tolist()))
)

# Merge df1 with df2 to get the port_id
df = df.merge(df_foreign_port[['Foreign_Port_Name_a', 'Latitude','Longitude']], left_on='mapped_port_name', right_on='Foreign_Port_Name_a', how='left')

# # Drop the redundant 'port_name_y' column after merge
# df1.drop(columns=['port_name_y'], inplace=True)

# # Rename columns for clarity
# df1.rename(columns={'port_name_x': 'original_port_name', 'port_id': 'mapped_port_id'}, inplace=True)

# =============================================================================
# output
# =============================================================================
df.to_csv(output_folder+"USACE_PORT_Foreign_to_FAF_Zone_801-802.csv",index=False)


