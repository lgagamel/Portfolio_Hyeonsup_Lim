import geopandas as gpd
import warnings
import pandas as pd
warnings.filterwarnings("ignore")

# input parameters
mode_prefix = "W"

# =============================================================================
# # Load shapefiles
# =============================================================================
RORO_nodes_gdf = gpd.read_file('../../__INPUT__/Water/NTAD_Intermodal_Freight_Facilities_Marine_Roll_on_Roll_off/Intermodal_Freight_Facilities_Marine_Roll-on_Roll-off.shp')
nodes_gdf = gpd.read_file('../../__INPUT__/Water/Navigable_Waterway_Network_Nodes/Waterway_Network_Node.shp')
links_gdf = gpd.read_file('../../__INPUT__/Water/Navigable_Waterway_Network_Lines/Waterway_Network.shp')
principal_port_nodes_gdf = gpd.read_file('../../__INPUT__/Water/USACE_Principal_Port/Principal_Ports/Principal_Ports.shp')

# =============================================================================
# merge link_tons
# =============================================================================
# link_tons_gdf = gpd.read_file('../../__INPUT__/Water/USACE_linktons/2017/linkton17.shp')
# link_tons_gdf = link_tons_gdf[["LINKNUM","TOTALUP","TOTALDOWN"]]
# links_gdf_test = links_gdf.merge(link_tons_gdf,on=["LINKNUM"],how="outer")
# links_gdf_test.drop(columns=["geometry"]).to_csv("output/01/links_gdf_test.csv",index=False)
# links_gdf = links_gdf.merge(link_tons_gdf,on=["LINKNUM"],how="left")


link_tons_gdf = gpd.read_file('../../__INPUT__/Water/BTS_Water_Network_Input/link_tons/Link_tonnages.shp')
link_tons_gdf["LINKNUM"] = link_tons_gdf["LINK"].astype(int)
link_tons_gdf = link_tons_gdf[["LINKNUM","TOTALUP","TOTALDOWN"]]
link_tons_gdf = link_tons_gdf.groupby(["LINKNUM"],as_index=False)[["TOTALUP","TOTALDOWN"]].mean()
links_gdf_test = links_gdf.merge(link_tons_gdf,on=["LINKNUM"],how="outer")
links_gdf_test.drop(columns=["geometry"]).to_csv("output/01/links_gdf_test.csv",index=False)
links_gdf = links_gdf.merge(link_tons_gdf,on=["LINKNUM"],how="left")


# =============================================================================
# convert CRS
target_CRS = 'EPSG:5070'
RORO_nodes_gdf = RORO_nodes_gdf.to_crs(target_CRS)
nodes_gdf = nodes_gdf.to_crs(target_CRS)
links_gdf = links_gdf.to_crs(target_CRS)
principal_port_nodes_gdf = principal_port_nodes_gdf.to_crs(target_CRS)

# nodes_gdf
nodes_gdf['ID'] = nodes_gdf['NODENUM'].astype(int).astype(str)
nodes_gdf['node_id'] = mode_prefix + nodes_gdf['ID']

# links_gdf
ind = links_gdf["ID"].isnull()
links_gdf = links_gdf.loc[~ind]
links_gdf[['ID','ANODE','BNODE']] = links_gdf[['ID','ANODE','BNODE']].astype(int).astype(str)
links_gdf['node_A'] = mode_prefix + links_gdf['ANODE']
links_gdf['node_B'] = mode_prefix + links_gdf['BNODE']
links_gdf['link_id'] = mode_prefix + links_gdf['ID']
links_gdf['distance'] = links_gdf['LENGTH']


# remove nodes with no connection to any links
good_nodes_list = list(links_gdf['node_A'])+list(links_gdf['node_B'])
good_nodes_list = list(set(good_nodes_list))
ind = nodes_gdf["node_id"].isin(good_nodes_list)
# check = 'W55010' in list(nodes_gdf.loc[~ind,"node_id"])
# raise()
# print(sum(ind)/len(ind),sum(~ind))
nodes_gdf = nodes_gdf.loc[ind]

# principal_port_nodes_gdf
port_gdf = principal_port_nodes_gdf[["PORT","PORT_NAME","TOTAL","EXPORTS","IMPORTS","DOMESTIC","geometry"]].copy()
port_gdf["principal_port"] = 1
port_gdf["roro_port"] = 0
RORO_nodes_gdf = RORO_nodes_gdf.rename(columns={"PORT":"RORO_NAME"})
port_gdf = gpd.sjoin_nearest(port_gdf, RORO_nodes_gdf[["RORO_NAME","geometry"]], how="left", distance_col="distance")
port_gdf["distance"] = port_gdf["distance"] * 0.000621371
ind = port_gdf["distance"]<20
port_gdf.loc[ind,"roro_port"]=1
port_gdf = port_gdf.drop(columns=["index_right","distance"])

# add RORO_nodes_gdf
port_gdf_roro = gpd.sjoin_nearest(RORO_nodes_gdf[["geometry"]], principal_port_nodes_gdf[["geometry"]], how="left", distance_col="distance")
port_gdf_roro["distance"] = port_gdf_roro["distance"] * 0.000621371
ind = port_gdf_roro["distance"]>20
port_gdf_roro = port_gdf_roro.loc[ind]
port_gdf_roro = port_gdf_roro.drop(columns=["index_right","distance"])
port_gdf = pd.concat([port_gdf,port_gdf_roro])
port_gdf["principal_port"] = port_gdf["principal_port"].fillna(0)
port_gdf["roro_port"] = port_gdf["roro_port"].fillna(1)
port_gdf["node_id_p"] = range(len(port_gdf))
port_gdf["node_id_p"] = "P" + port_gdf["node_id_p"].astype(str)


# map ports to nodes
port_gdf = gpd.sjoin_nearest(port_gdf, nodes_gdf[["node_id","geometry"]], how="left", distance_col="dist_p2w")
port_gdf["dist_p2w"] = port_gdf["dist_p2w"] * 0.000621371
# port_gdf = port_gdf.drop(columns=["index_right","dist_p2w"])
port_gdf = port_gdf.drop(columns=["index_right"])

ind = port_gdf["TOTAL"].isnull()
port_gdf["TOTAL_imputed"] = 0
port_gdf.loc[ind,"TOTAL_imputed"] = 1
port_gdf.loc[ind,"TOTAL"] = port_gdf["TOTAL"].min()/2

# =============================================================================
# output
# =============================================================================
nodes_gdf.to_file('output/01/water_nodes.shp')
links_gdf.to_file('output/01/water_links.shp')
port_gdf.to_file('output/01/ports.shp')
principal_port_nodes_gdf.to_file('output/01/principal_ports.shp')
RORO_nodes_gdf.to_file('output/01/roro_ports.shp')

nodes_gdf = nodes_gdf.drop(columns=["geometry"])
links_gdf = links_gdf.drop(columns=["geometry"])
port_gdf = port_gdf.drop(columns=["geometry"])
principal_port_nodes_gdf = principal_port_nodes_gdf.drop(columns=["geometry"])
RORO_nodes_gdf = RORO_nodes_gdf.drop(columns=["geometry"])

nodes_gdf.to_csv('output/01/water_nodes.csv',index=False)
links_gdf.to_csv('output/01/water_links.csv',index=False)
port_gdf.to_csv('output/01/ports.csv',index=False)
principal_port_nodes_gdf.to_csv('output/01/principal_ports.csv',index=False)
RORO_nodes_gdf.to_csv('output/01/roro_ports.csv',index=False)