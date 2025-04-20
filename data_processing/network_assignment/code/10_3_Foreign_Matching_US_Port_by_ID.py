import warnings
warnings.filterwarnings("ignore")
import geopandas as gpd
import pandas as pd

input_folder = "output/10/10_2/"
output_folder = "output/10/10_3/"

# =============================================================================
# # Load shapefiles
# =============================================================================
df = pd.read_csv(input_folder+"USACE_PORT_US.csv")
principal_port_nodes_gdf = gpd.read_file('output/06/ports.shp')

principal_port_nodes_gdf["PORT_NAMEP"] = principal_port_nodes_gdf["PORT_NAME"]
ind = principal_port_nodes_gdf['PORT_NAMEP'].isnull()
principal_port_nodes_gdf.loc[ind,'PORT_NAMEP'] = principal_port_nodes_gdf.loc[ind,'RORO_NAME']
principal_port_nodes_gdf = principal_port_nodes_gdf[['PORT', 'PORT_NAMEP','node_id_p']]


# df = df.merge(principal_port_nodes_gdf,on=["PORT"],how="outer")
# =============================================================================
# port matching by ID
# =============================================================================
df = df.merge(principal_port_nodes_gdf,on=["PORT"],how="left")
df.to_csv(output_folder+"USACE_PORT_US_Match_by_ID.csv",index=False)

