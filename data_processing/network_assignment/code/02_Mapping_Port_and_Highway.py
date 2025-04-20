import warnings
warnings.filterwarnings("ignore")
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd


# =============================================================================
# # Load shapefiles
# =============================================================================
port_gdf = gpd.read_file('output/01/ports.shp')
truck_gdf = gpd.read_file('output/01/truck_nodes.shp')
water_gdf = gpd.read_file('output/01/water_nodes.shp')


# =============================================================================
# mapping nearest
# =============================================================================
port_gdf = port_gdf.rename(columns={"node_id":"node_id_w"})
truck_gdf = truck_gdf.rename(columns={"node_id":"node_id_t"})
port_gdf = gpd.sjoin_nearest(port_gdf, truck_gdf[["node_id_t","geometry"]], how="left", distance_col="dist_p2t")
port_gdf["dist_p2t"] = port_gdf["dist_p2t"] * 0.000621371
print(port_gdf["dist_p2t"].max())
# port_gdf = port_gdf.drop(columns=["index_right","dist_p2t"])
port_gdf = port_gdf.drop(columns=["index_right"])



# =============================================================================
# port to water link
# =============================================================================
node_id_p_list = []
node_id_w_list = []
geometry_list = []
for i,row in port_gdf.iterrows():
    print(row["node_id_w"], row["node_id_p"])

    point_A = port_gdf[port_gdf['node_id_p'] == row["node_id_p"]]
    point_B = water_gdf[water_gdf['node_id'] == row["node_id_w"]]

    # Extract the geometry of the points
    geom_A = point_A.geometry.values[0]
    geom_B = point_B.geometry.values[0]
    
    # Step 3: Create a Line Connecting the Points
    line = LineString([geom_A, geom_B])
    
    node_id_p_list.append(row["node_id_p"])
    node_id_w_list.append(row["node_id_w"])
    geometry_list.append(line)

# Step 4: Create a GeoDataFrame for the Link Layer
target_CRS = 'EPSG:5070'
link_gdf = gpd.GeoDataFrame({'node_id_p': node_id_p_list, 
                             'node_id_w': node_id_w_list, 
                             'geometry': geometry_list}, 
                            crs=target_CRS)

link_gdf["link_id"] = range(len(link_gdf))
link_gdf["link_id"] = "PW" + link_gdf["link_id"].astype(str)
port_gdf["link_id_PW"] = link_gdf["link_id"]
link_gdf.to_file('output/02/port_to_water_link.shp')



# =============================================================================
# port to truck link
# =============================================================================
node_id_p_list = []
node_id_t_list = []
geometry_list = []
for i,row in port_gdf.iterrows():
    print(row["node_id_t"], row["node_id_t"])

    point_A = port_gdf[port_gdf['node_id_p'] == row["node_id_p"]]
    point_B = truck_gdf[truck_gdf['node_id_t'] == row["node_id_t"]]

    # Extract the geometry of the points
    geom_A = point_A.geometry.values[0]
    geom_B = point_B.geometry.values[0]
    
    # Step 3: Create a Line Connecting the Points
    line = LineString([geom_A, geom_B])
    
    node_id_p_list.append(row["node_id_p"])
    node_id_t_list.append(row["node_id_t"])
    geometry_list.append(line)

# Step 4: Create a GeoDataFrame for the Link Layer
target_CRS = 'EPSG:5070'
link_gdf = gpd.GeoDataFrame({'node_id_p': node_id_p_list, 
                             'node_id_t': node_id_t_list, 
                             'geometry': geometry_list}, 
                            crs=target_CRS)

link_gdf["link_id"] = range(len(link_gdf))
link_gdf["link_id"] = "PT" + link_gdf["link_id"].astype(str)
port_gdf["link_id_PT"] = link_gdf["link_id"]
link_gdf.to_file('output/02/port_to_truck_link.shp')





# =============================================================================
# output
# =============================================================================
port_gdf.to_file('output/02/ports_before.shp')
ind = port_gdf["dist_p2t"]<1000
port_gdf = port_gdf.loc[ind]
port_gdf.to_file('output/02/ports.shp')
port_gdf.drop(columns=["geometry"]).to_csv('output/02/ports.csv',index=False)




