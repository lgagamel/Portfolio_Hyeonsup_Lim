import pandas as pd
from math import radians, cos, sin, asin, sqrt
import math 
import numpy as np

# =============================================================================
# Read data
# =============================================================================
df = pd.read_csv("output/step_5/TMAS2019_faf5.csv")

# =============================================================================
# columns
# =============================================================================
# ['State_Code', 'Station_Id', 'Travel_Dir', 'ID_S', 'BN_S', 'EN_S','AADT', 'AADT_COMBI', 'AADT_SINGL']


# =============================================================================
# select only matched records - remove null records
# =============================================================================
ind = df["ID_S"].isnull()
df = df.loc[~ind]

# =============================================================================
# remove two direction combined records
# =============================================================================
ind = df["Travel_Dir"].isin([0,9])
df = df.loc[~ind]

# =============================================================================
# changed dtype to int
# =============================================================================
int_columns = ['State_Code','Travel_Dir','ID_S', 'BN_S', 'EN_S','DIR', 'Class']
df[int_columns] = df[int_columns].astype(int)


# =============================================================================
# load node location 
# =============================================================================
df_node_list = pd.read_csv("output/step_2/node_list.csv",index_col=["ID"])

# =============================================================================
# calculate distance between o-d
# =============================================================================
# Python 3 program to calculate Distance Between Two Points on Earth
def distance(origin, destination):
    lat1,lon1 = origin
    lat2,lon2 = destination
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return (c * r)

def get_dx_dy(origin, destination):
    mid = [(origin[0]+destination[0])/2,
           (origin[1]+destination[1])/2] 
    origin_x = [mid[0],origin[1]]
    destination_x = [mid[0],destination[1]]

    origin_y = [origin[0],mid[1]]
    destination_y = [destination[0],mid[1]]


    # driver code
    dx = distance(origin_x,destination_x)
    dy = distance(origin_y,destination_y)
    
    if destination[1]<origin[1]:
        dx = -dx
    
    if destination[0]<origin[0]:
        dy = -dy
    return dx, dy

# =============================================================================
# calculate angle and find nearest direction
# =============================================================================
# https://www.analytics-link.com/post/2018/08/21/calculating-the-compass-direction-between-two-points-in-python
# 1 North
# 2 Northeast
# 3 East
# 4 Southeast
# 5 South
# 6 Southwest
# 7 West
# 8 Northwest
# 9 North-South or Northeast-Southwest combined (ATR stations only)
# 0 East-West or Southeast-Northwest combined (ATR stations only)

tmas_compass_degrees ={"1a":0,"2":45,"3":90,"4":135,"5":180,
                  "6":225,"7":270,"8":315,"1b":360}

def direction_lookup(dx, dy):
    degrees_temp = math.atan2(dx, dy)/math.pi*180

    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:
        degrees_final = degrees_temp

    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    compass_lookup = round(degrees_final / 45)
    return compass_brackets[compass_lookup], degrees_final


# =============================================================================
# Main Loop
# =============================================================================
origin_nodes = np.zeros(len(df))
destination_nodes = np.zeros(len(df))
for i in range(len(df)):
    a = df.iloc[i]["BN_S"]
    b = df.iloc[i]["EN_S"]
    tmas_direction = str(df.iloc[i]["Travel_Dir"])
    
    origin = [df_node_list.loc[a,"Latitude"]/100000,df_node_list.loc[a,"Longitude"]/100000]
    destination = [df_node_list.loc[b,"Latitude"]/100000,df_node_list.loc[b,"Longitude"]/100000]
    
    
    if tmas_direction == "1":
        tmas_degree = [tmas_compass_degrees[tmas_direction+"a"],tmas_compass_degrees[tmas_direction+"b"]]
    else:
        tmas_degree = tmas_compass_degrees[tmas_direction]
    tmas_degree = np.array(tmas_degree)
    
    
    dx, dy = get_dx_dy(origin,destination)
    direction,degree = direction_lookup(dx, dy)
    degree_dif1 = np.min(np.abs(degree-tmas_degree))
    
    
    dx, dy = get_dx_dy(destination,origin)
    direction,degree = direction_lookup(dx, dy)
    degree_dif2 = np.min(np.abs(degree-tmas_degree))
    
    if degree_dif1<degree_dif2:
        origin_final = a
        destination_final = b
    else:
        origin_final = b
        destination_final = a
    origin_nodes[i] = origin_final
    destination_nodes[i] = destination_final
    
df["Node_O"] = origin_nodes
df["Node_D"] = destination_nodes

# =============================================================================
# 
# =============================================================================
int_columns = ['ID_S', 'BN_S', 'EN_S', 'DIR','Class','Node_O','Node_D']
df[int_columns] = df[int_columns].astype(int)
df.to_csv("output/step_6/TMAS2019_faf5.csv",index=False)