import pandas as pd
import geopandas as gpd

# =============================================================================
# read data
# =============================================================================
df = pd.read_csv("output/03/truck_port_to_centroid_skim.csv")
truck_node_gdf = gpd.read_file('output/01/truck_nodes.shp')

# =============================================================================
# top 10 ports for each centroid node from highway
# =============================================================================
df = df.groupby('node_id_t').apply(lambda x: x.sort_values(by="hour",ascending=True).head(10))
df = df.reset_index(drop=True)

# =============================================================================
# get centroids with no connections to ports
# =============================================================================
df["null"] = (df["hour"].isnull())*1
df_grp = df.groupby(["node_id_t"],as_index=False)["null"].sum()
ind = df_grp["null"]==10
df_grp = df_grp.loc[ind]
truck_node_gdf = truck_node_gdf.rename(columns={"node_id":"node_id_t"})
truck_node_gdf = df_grp.merge(truck_node_gdf,on=["node_id_t"],how="left")
truck_node_gdf = gpd.GeoDataFrame(truck_node_gdf)
truck_node_gdf.to_file("output/04/centorids_with_no_ports.shp")

# =============================================================================
# output
# =============================================================================
df = df.dropna()
df.to_csv("output/04/truck_port_to_centroid_skim_only_feasible.csv",index=False)

