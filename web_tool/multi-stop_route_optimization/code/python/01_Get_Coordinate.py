import pandas as pd
import pickle
import numpy as np
import time
import sys
from geopy.geocoders import Nominatim
from math import radians, sin, cos, acos
geolocator = Nominatim(user_agent="bb")

# =============================================================================
# parameters
# =============================================================================
buffer = 0.1
interval = 0.1



def address_2_coordinate_main(df_address_xy,address_split):
    yx = [np.nan,np.nan]
    for i in range(min(len(address_split)-1,5)):
        address = " ".join(address_split[:len(address_split)-i])
        try:
            yx = address_2_coordinate_from_prev_list(df_address_xy, address)
        except:
            yx = address_2_coordinate_by_nominatim(address)
            if len(yx)>0:
                append_address_xy(address,*yx)
        print(address,i,yx)
        if len(yx)>0:
            return yx
    return yx

def append_address_xy(address,y,x):
    with open("../network/_address/address_xy.csv", "a") as f:
        address = '"' + address + '"'
        line = ",".join([address,str(x),str(y)]) + "\n"
        f.write(line)

def address_2_coordinate_from_prev_list(df_address_xy, address):
    x = df_address_xy.loc[address]["x"]
    y = df_address_xy.loc[address]["y"]
    yx = [y,x]
    return yx


def address_2_coordinate_by_nominatim(address):
    try:
        time.sleep(1)
        loc = geolocator.geocode(address, exactly_one=True)        
        return [loc.latitude,loc.longitude]
    except:
        return []


# opening the file in read mode
with open("output/00/address.txt","r") as f:
    # reading the file
    address_list = f.read()
    # splitting the text it further when '.' is seen.
    address_list = address_list.split('\n')

address_list = [x for x in address_list if len(x)>0]


# =============================================================================
# Main
# =============================================================================
df_address_xy = pd.read_csv("../network/_address/address_xy.csv",index_col="address",dtype={"address":str})
yx_all = []
start = time.time()
for address in address_list:
    end = time.time()
    elapsed_time = end - start
    if elapsed_time>1000:
        raise("taking too long 1")

    if len(address)<=3:
        yx = [np.nan,np.nan]
    else:
        address = address.replace(","," ").replace("\t"," ").replace(":"," ").replace("|"," ")
        for __i__ in range(50):
            address = address.replace("  "," ")
        address_split = address.split(" ")
        if len(address_split)==2:
            try:
                yx = [float(x) for x in address_split]
            except:
                yx = address_2_coordinate_main(df_address_xy,address_split)
        else:
            yx = address_2_coordinate_main(df_address_xy,address_split)
    yx = [address] + yx
    yx_all = yx_all + [yx]

# =============================================================================
# write yx output
# =============================================================================
df_xy_all = pd.DataFrame(yx_all,columns=["address","y","x"])
df_xy_all["i"] = range(len(df_xy_all))
df_xy_all.to_csv("output/01/xy_all.csv",index=False)
ind = df_xy_all["x"].isnull()
df_xy_all.loc[ind].to_csv("output/01/xy_null.csv",index=False)
df_xy = df_xy_all.dropna()
df_xy["i"] = range(len(df_xy))
df_xy.to_csv("output/01/xy.csv",index=False)

# =============================================================================
# get center_point_of_xy
# =============================================================================
center_point_of_xy = []
for i in range(len(df_xy)):
    x = df_xy.iloc[i]["x"]
    y = df_xy.iloc[i]["y"]
    x = round(x,1)
    y = round(y,1)
    center_point_of_xy = center_point_of_xy + [(y,x)]

outputfilename = "output/01/center_point_of_xy.pkl"
with open(outputfilename, 'wb') as f:
     pickle.dump(center_point_of_xy, f)

# =============================================================================
# create distance df
# =============================================================================
df_o = df_xy.copy()
df_d = df_xy.copy()
df_o = df_o[["i","x","y"]]
df_o.columns = ["o_i","o_x","o_y"]
df_o["dummy"] = 0
df_d = df_d[["i","x","y"]]
df_d.columns = ["d_i","d_x","d_y"]
df_d["dummy"] = 0
df_dist = df_o.merge(df_d,on=["dummy"],how="outer")
df_dist = df_dist.drop(columns=["dummy"])


# =============================================================================
# get distance where gcd is greater than X
# =============================================================================
def gcd(lon1, lat1, lon2, lat2):
    if abs(lon2-lon1)+abs(lat2-lat1)==0:
        gcd_final = 0
    else:
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        gcd_final = 3958.756 * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))
    return gcd_final

df_dist['gcd'] = df_dist.apply(lambda e: gcd(e.o_x, e.o_y, e.d_x, e.d_y), axis=1)


# =============================================================================
# create center_point_list
# =============================================================================
center_point_list = []
df_center_point = pd.read_csv("../network/_network_simple_entire/us_center_point_to_nodes_updated.csv",dtype={"ID":str})
def get_center_point_list(o_x,o_y,d_x,d_y,gcd,o_i,d_i):
    global center_point_list
    if (o_i==d_i):
        simple_dist = 0
    elif (gcd<10):
        x_min = round(min(o_x,d_x)-buffer,1)
        x_max = round(max(o_x,d_x)+buffer,1)
        y_min = round(min(o_y,d_y)-buffer,1)
        y_max = round(max(o_y,d_y)+buffer,1)
        
        x_list = np.arange(x_min, x_max+0.01, interval)
        y_list = np.arange(y_min, y_max+0.01, interval)
        for x in x_list:
            for y in y_list:
                x = round(x,1)
                y = round(y,1)
                if (y,x) in center_point_list:
                    print("skipped",(y,x))
                else:
                    print("added",(y,x))
                    center_point_list = center_point_list + [(y,x)]
        simple_dist = np.nan
    else:        
        ind = np.argmin((df_center_point["x"]-o_x)**2+(df_center_point["y"]-o_y)**2)
        current_dist_set = {}
        if ind<len(df_center_point):
            incremental = 1
        else:
            incremental = -1
        while len(current_dist_set)==0:
            try:
                tmp_o = str(df_center_point.iloc[ind]["y"]) + str(df_center_point.iloc[ind]["x"])
                with open("../network/_network_simple_dist/"+tmp_o+".pkl", 'rb') as f:
                    current_dist_set = pickle.load(f)
            except:
                ind = int(ind + incremental)
                pass
        ind = np.argmin((df_center_point["x"]-d_x)**2+(df_center_point["y"]-d_y)**2)
        try:
            tmp_d = str(df_center_point.iloc[ind]["y"]) + str(df_center_point.iloc[ind]["x"])        
            simple_dist = current_dist_set[tmp_d] * gcd
        except:            
            tmp_f_list = list(current_dist_set.values())
            tmp_f_list = [e for e in tmp_f_list if e>0]
            tmp_f = np.mean(tmp_f_list)
            simple_dist = tmp_f * gcd
            
    return simple_dist

df_dist["simple_dist"] = df_dist.apply(lambda e: get_center_point_list(e.o_x, e.o_y, e.d_x, e.d_y, e.gcd,e.o_i,e.d_i) , axis=1)

df_dist.to_csv("output/01/xy_gcd.csv",index=False)

outputfilename = "output/01/center_point_list.pkl"
with open(outputfilename, 'wb') as f:
     pickle.dump(center_point_list, f)
         
