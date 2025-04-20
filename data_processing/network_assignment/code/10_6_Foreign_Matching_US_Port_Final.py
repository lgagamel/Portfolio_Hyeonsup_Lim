import warnings
warnings.filterwarnings("ignore")
import pandas as pd

output_folder = "output/10/10_6/"

# =============================================================================
# # Load shapefiles
# =============================================================================
df_us_port = pd.read_csv("output/10/10_2/USACE_PORT_US.csv")
df_id = pd.read_csv("output/10/10_4/USACE_PORT_US_Match_by_ID.csv")
df_name = pd.read_csv("output/10/10_5/USACE_PORT_US_Match_by_Name_Adj.csv")


# =============================================================================
# merge by id
# =============================================================================
df_id = df_id[["STATE","PORT","node_id_p"]]
df_us_port = df_us_port.merge(df_id,on=["STATE","PORT"],how="left")


# =============================================================================
# merge by name
# =============================================================================
df_name = df_name.rename(columns={"node_id_p_adj":"node_id_p_name"})
df_name = df_name[["STATE","PORT_NAME","node_id_p_name"]]
df_us_port = df_us_port.merge(df_name,on=["STATE","PORT_NAME"],how="left")


# =============================================================================
# fill node_id_p_name if node_id_p is null
# =============================================================================
ind = df_us_port["node_id_p"].isnull()
df_us_port.loc[ind,"node_id_p"] = df_us_port.loc[ind,"node_id_p_name"]
df_us_port["match_type"] = "PORT"
df_us_port.loc[ind,"match_type"] = "PORT_NAME"


# =============================================================================
# output
# =============================================================================
df_us_port = df_us_port.drop(columns=["node_id_p_name"])
df_us_port.to_csv(output_folder+"USACE_PORT_US_Match.csv",index=False)

# =============================================================================
# check
# =============================================================================
df_us_port["cnt"]=1
df_us_port = df_us_port.groupby(['STATE','PORT', 'PORT_NAME'],as_index=False)['cnt'].sum()
df_us_port.to_csv(output_folder + "check.csv",index=False) 

