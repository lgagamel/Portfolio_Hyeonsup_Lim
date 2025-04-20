import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString

intput_folder = "output/10/10_13/"
# output_folder = "output/10/10_14/"
output_folder = "output/10/"

# =============================================================================
# create mapping between foreign centroids to water nodes from 10_13
# =============================================================================

region_list = [
    "F801w",
    "F801e",
    "F801g",
    "F802w",
    "F802e",
    "F803",
    "F804-805",
    "F806-808",
    ]

df_mapping = pd.DataFrame()
for region in region_list:
    gdf = gpd.read_file(intput_folder + region + ".shp")
    df = gdf[["node_id"]]
    df["node_id_f"] = region    
    df_mapping = pd.concat([df_mapping,df])


# Load node shapefiles
gdf_f = gpd.read_file('output/10/10_12/foreign_centroid.shp')
gdf_w = gpd.read_file('output/01/water_nodes.shp')

# convert CRS
target_CRS = 'EPSG:4326'
gdf_f = gdf_f.to_crs(target_CRS)
gdf_w = gdf_w.to_crs(target_CRS)


df_mapping["node_id_f"] = df_mapping["node_id_f"].apply(lambda x: x.replace("-","~"))
gdf_f["node_id_f"] = gdf_f["node_id_f"].apply(lambda x: x.replace("-","~"))


gdf_f.to_file(output_folder + 'foreign_centroid.shp')
gdf_w.to_file(output_folder + 'water_nodes.shp')

gdf_f = gdf_f[["node_id_f","geometry"]]
gdf_w = gdf_w[["node_id","geometry"]]

# Merge shapefiles with the mapping on the node IDs
gdf = pd.merge(df_mapping, gdf_f, on='node_id_f')
gdf = pd.merge(gdf, gdf_w, on='node_id', suffixes=('_1', '_2'))


# Create a GeoDataFrame with LineString geometry
gdf = gpd.GeoDataFrame(gdf, geometry=[
    LineString([(row['geometry_1'].x, row['geometry_1'].y), (row['geometry_2'].x, row['geometry_2'].y)])
    for idx, row in gdf.iterrows()], crs=target_CRS)

# Save the link layer as a new shapefile
gdf = gdf[['node_id', 'node_id_f', 'geometry']]
gdf.to_file(output_folder + 'foreign_centroid_link.shp')
gdf.drop(columns=["geometry"]).to_csv(output_folder + 'foreign_centroid_link.csv',index=False)
