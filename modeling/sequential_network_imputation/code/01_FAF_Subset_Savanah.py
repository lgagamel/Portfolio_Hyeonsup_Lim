import geopandas
import pandas as pd

# =============================================================================
# Load data
# =============================================================================
df = geopandas.read_file(r'C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\01.FAF\03.Network_Assignment\FAF5_Model_Highway_Network\Networks\Shapefile\FAF5_links.shp')
df_truck_2017_CU = pd.read_csv(r"C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\01.FAF\03.Network_Assignment\FAF5_2017_HighwayAssignmentResults_04_07_2022\Assignment Flow Tables\CSV Format\FAF5 Total CU Truck Flows by Commodity_2017.csv")
df_truck_2017_SU = pd.read_csv(r"C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\01.FAF\03.Network_Assignment\FAF5_2017_HighwayAssignmentResults_04_07_2022\Assignment Flow Tables\CSV Format\FAF5 Total SU Truck Flows by Commodity_2017.csv")
df_truck_2017_TOT = pd.read_csv(r"C:\Users\9hl\Dropbox (Personal)\ORNL\21.Data\01.FAF\03.Network_Assignment\FAF5_2017_HighwayAssignmentResults_04_07_2022\Assignment Flow Tables\CSV Format\FAF5 Total Truck Flows by Commodity_2017.csv")

# =============================================================================
# list of columns
# =============================================================================
# ['OBJECTID',
#  'ID',
#  'LENGTH',
#  'DIR',
#  'DATA',
#  'VERSION',
#  'Class',
#  'Class_Desc',
#  'Road_Name',
#  'Sign_Rte',
#  'Rte_Type',
#  'Rte_Number',
#  'Rte_Qualif',
#  'Country',
#  'STATE',
#  'STFIPS',
#  'County_Nam',
#  'CTFIPS',
#  'Urban_Code',
#  'FAFZONE',
#  'Status',
#  'F_Class',
#  'Facility_T',
#  'NHS',
#  'STRAHNET',
#  'NHFN',
#  'Truck',
#  'AB_Lanes',
#  'BA_Lanes',
#  'Speed_Limi',
#  'Toll_Type',
#  'Toll_Name',
#  'Toll_Link',
#  'Toll_Link_',
#  'HPMS_USA_R',
#  'HPMS_Begin',
#  'HPMS_End_P',
#  'BorderStat',
#  'BorderSt_1',
#  'BorderFAF1',
#  'BorderFAF2',
#  'TRUCKTOLL',
#  'BorderLink',
#  'AddedBorde',
#  'AdjustSpee',
#  'AdjustReas',
#  'AB_FinalSp',
#  'BA_FinalSp',
#  'AB_Combine',
#  'BA_Combine',
#  'AB_FreeFlo',
#  'BA_FreeFlo',
#  'SHAPE_Leng',
#  'geometry']

# =============================================================================
# selected columns
# =============================================================================
df = df[['OBJECTID', 'ID','LENGTH','DIR','Class','Speed_Limi','geometry']]


# =============================================================================
# truck volume columns
# =============================================================================
# df_truck_2017_CU = df_truck_2017_CU[['ID', 'AB Trips_17 CU','BA Trips_17 CU', 'TOT Trips_17 CU']]
# df_truck_2017_CU.columns = ['ID', 'AB_17 CU','BA_17 CU', 'TOT_17 CU']
# df_truck_2017_SU = df_truck_2017_SU[['ID', 'AB Trips_17 SU','BA Trips_17 SU', 'TOT Trips_17 SU']]
# df_truck_2017_SU.columns = ['ID', 'AB_17 SU','BA_17 SU', 'TOT_17 SU']
# df_truck_2017_TOT = df_truck_2017_TOT[['ID', 'AB Trips_17 All','BA Trips_17 All','TOT Trips_17 All']]
# df_truck_2017_TOT.columns = ['ID', 'AB_17 All','BA_17 All', 'TOT_17 All']

# df_truck_2017_CU = df_truck_2017_CU[['ID','TOT Tons_17 CU','TOT Trips_17 CU']]
# df_truck_2017_CU.columns = ['ID', 'Tons17 CU', 'Trip17 CU']
# df_truck_2017_SU = df_truck_2017_SU[['ID', 'TOT Tons_17 SU','TOT Trips_17 SU']]
# df_truck_2017_SU.columns = ['ID', 'Tons17 SU', 'Trip17 SU']
# df_truck_2017_TOT = df_truck_2017_TOT[['ID','TOT Tons_17 All','TOT Trips_17 All']]
# df_truck_2017_TOT.columns = ['ID', 'Tons17 All', 'Trip17 All']

df_truck_2017_TOT = df_truck_2017_TOT[['ID', 'AB Trips_17 All','BA Trips_17 All','TOT Trips_17 All']]
df_truck_2017_TOT.columns = ['ID', 'AB_17_All','BA_17_All', 'TOT_17_All']


# =============================================================================
# merge
# =============================================================================
# df = df.merge(df_truck_2017_CU,on="ID",how="left")
# df = df.merge(df_truck_2017_SU,on="ID",how="left")
df = df.merge(df_truck_2017_TOT,on="ID",how="left")

# =============================================================================
# dtype
# =============================================================================
df["OBJECTID"] = df["OBJECTID"].astype(int)
df[["Class","Speed_Limi","AB_17_All","BA_17_All","TOT_17_All"]] = df[["Class","Speed_Limi","AB_17_All","BA_17_All","TOT_17_All"]].fillna(0)
df[["Class","Speed_Limi"]] = df[["Class","Speed_Limi"]].astype(int)

# =============================================================================
# output
# =============================================================================
# df.to_file("output/step_1/FAF5_network.shp")


# =============================================================================
# region
# =============================================================================
from shapely.geometry import Point
s = geopandas.GeoSeries([Point(-81.15106688133065, 32.12894157327287)])
gdf_region = geopandas.GeoDataFrame(index=[0], crs='epsg:4326', geometry=s)
gdf_region["buffer"]=1
gdf_region = gdf_region.to_crs(crs="EPSG:3857")
gdf_region["geometry"] = gdf_region["geometry"].buffer(804672) # meters (500 miles)
# gdf_region.to_file("output/step_1/buffer.shp")


# =============================================================================
# clip
# =============================================================================
df = df.to_crs(crs="EPSG:3857")
# df_clip = geopandas.clip(df, gdf_region)
df_clip = df.sjoin(gdf_region)
df_clip = df_clip.drop(columns=['index_right', 'buffer'])

df_clip.to_file("output/step_1/FAF5_network_Savanah.shp")