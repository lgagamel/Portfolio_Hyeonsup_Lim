import warnings
warnings.filterwarnings("ignore")

import geopandas as gpd
import pandas as pd

# input parameters
mode_prefix = "T"

# =============================================================================
# # Load data from CSV files
# =============================================================================
nodes_gdf = gpd.read_file('../../__INPUT__/Truck/FAF5_Network_with_MMnodes_shp/FAF5_Nodes_withMM.shp')
links_gdf = gpd.read_file('../../__INPUT__/Truck/FAF5_Network_with_MMnodes_shp/FAF5_Links_withAB_MM.shp')
county_gdf = gpd.read_file('../../__INPUT__/county/tl_2017_us_county/tl_2017_us_county.shp')



# =============================================================================
# convert CRS
target_CRS = 'EPSG:5070'
nodes_gdf = nodes_gdf.to_crs(target_CRS)
links_gdf = links_gdf.to_crs(target_CRS)
county_gdf = county_gdf.to_crs(target_CRS)

# =============================================================================
# add prefix to ID
# =============================================================================
nodes_gdf['node_id'] = mode_prefix + nodes_gdf['ID'].astype(str)
links_gdf['node_A'] = mode_prefix + links_gdf['FROM_ID'].astype(str)
links_gdf['node_B'] = mode_prefix + links_gdf['TO_ID'].astype(str)
links_gdf['link_id'] = mode_prefix + links_gdf['ID'].astype(str)
links_gdf['distance'] = links_gdf['LENGTH']


# =============================================================================
# centroids
# =============================================================================
ind = nodes_gdf["CENTROID"]==1
centroid_gdf = nodes_gdf.loc[ind].copy()
centroid_gdf = centroid_gdf[["node_id","CENTROID","CENTROIDID","geometry"]]
centroid_gdf["CENTROIDID"] = centroid_gdf["CENTROIDID"].astype(int)

county_gdf = county_gdf.rename(columns={"GEOID":"FIPS"})
county_gdf = county_gdf[["FIPS","geometry"]]
centroid_gdf = gpd.sjoin_nearest(centroid_gdf, county_gdf, how="left", distance_col="distance")
centroid_gdf["distance"] = centroid_gdf["distance"] * 0.000621371
print(centroid_gdf["distance"].max())
centroid_gdf = centroid_gdf.drop(columns=["index_right","distance"])

centroid_gdf.to_file('output/01/centroid.shp')
centroid_gdf = centroid_gdf.drop(columns=["geometry"])
centroid_gdf.to_csv('output/01/centroid.csv',index=False)



# =============================================================================
# output
# =============================================================================
nodes_gdf.to_file('output/01/truck_nodes.shp')
links_gdf.to_file('output/01/truck_links.shp')

nodes_gdf = nodes_gdf.drop(columns=["geometry"])
links_gdf = links_gdf.drop(columns=["geometry"])

nodes_gdf.to_csv('output/01/truck_nodes.csv',index=False)
links_gdf.to_csv('output/01/truck_links.csv',index=False)

