import warnings
warnings.filterwarnings("ignore")
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd


# =============================================================================
# # Load shapefiles
# =============================================================================
port_gdf = gpd.read_file('output/01/ports.shp')
water_gdf = gpd.read_file('output/01/water_nodes.shp')
centroids_with_no_ports_gdf = gpd.read_file("output/04/centorids_with_no_ports.shp")


# =============================================================================
# get new ports based on distance to centroids_with_no_ports_gdf
# =============================================================================
# water_gdf = water_gdf.rename(columns={"node_id":"node_id_w"})
added_port_gdf = gpd.sjoin_nearest(centroids_with_no_ports_gdf[["node_id_t","geometry"]], water_gdf[["node_id","geometry"]], how="left", distance_col="dist")
added_port_gdf = added_port_gdf.merge(water_gdf[['geometry']], left_on='index_right', right_index=True, suffixes=('', '_right'))
added_port_gdf['geometry'] = added_port_gdf['geometry_right']
added_port_gdf["dist"] = added_port_gdf["dist"] * 0.000621371
print(added_port_gdf["dist"].max())
# port_gdf = port_gdf.drop(columns=["index_right","dist_p2t"])
added_port_gdf = added_port_gdf.drop(columns=["index_right","geometry_right"])
added_port_gdf["node_id_p"] = range(len(added_port_gdf))
added_port_gdf["node_id_p"] = added_port_gdf["node_id_p"] + 154
added_port_gdf["node_id_p"] = "P" + added_port_gdf["node_id_p"].astype(str)
added_port_gdf["TOTAL"] = port_gdf["TOTAL"].min()
added_port_gdf["principal_"]=0
added_port_gdf["roro_port"]=0
added_port_gdf["dist_p2w"]=0
added_port_gdf["TOTAL_impu"]=1
added_port_gdf.to_file("output/05/added_port.shp")



# =============================================================================
# output combined port
# =============================================================================
added_port_gdf = added_port_gdf.drop(columns=["node_id_t","dist"])
port_gdf = pd.concat([port_gdf, added_port_gdf], ignore_index=True)
port_gdf = gpd.GeoDataFrame(port_gdf, geometry='geometry')
port_gdf.to_file("output/05/ports.shp")
