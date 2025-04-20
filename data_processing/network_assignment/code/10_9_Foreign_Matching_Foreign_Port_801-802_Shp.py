import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

output_folder = "output/10/10_9/"

df = pd.read_csv("output/10/10_8/USACE_PORT_Foreign_to_FAF_Zone_801-802.csv")

# Create a geometry column from the latitude and longitude
df['geometry'] = df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

# Convert the dataframe into a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')
target_CRS = 'EPSG:4326'
gdf = gdf.set_crs(target_CRS)

# Save as a shapefile
gdf.to_file(output_folder + "USACE_PORT_Foreign_to_FAF_Zone_801-802.shp")
