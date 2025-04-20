import pandas as pd
import numpy as np
import os

intput_folder = "output/13/"
output_folder = "output/14/"
inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "routing_" in e]

def quick_summary(df):
    summary = pd.DataFrame()
    summary['count'] = df.count()
    summary['nulls'] = df.isnull().sum()
    summary['infinite'] = np.isinf(df).sum()
    summary['mean'] = df.mean()
    summary['std'] = df.std()
    summary['min'] = df.min()
    summary['5th_percentile'] = df.quantile(0.05)
    summary['95th_percentile'] = df.quantile(0.95)
    summary['max'] = df.max()
    
    return summary

ver = "v1"

df_water = pd.read_csv('output/01/water_links.csv')
df_truck = pd.read_csv('output/01/truck_links.csv')

dict_water_distance = df_water.set_index('link_id')['distance'].to_dict()
dict_truck_distance = df_truck.set_index('link_id')['distance'].to_dict()

def get_water_distance(path):
    water_distance = 0
    for p in path:
        try:
            water_distance = water_distance + dict_water_distance[p]
        except:
            pass
    return water_distance

def get_truck_distance(path):
    truck_distance = 0
    for p in path:
        try:
            truck_distance = truck_distance + dict_truck_distance[p]
        except:
            pass
    return truck_distance

# get truck/water distance
def get_distance(path):
    try:
        path = path.split("-")
        water_distance = get_water_distance(path)
        truck_distance = get_truck_distance(path)
    except:
        truck_distance = np.nan
        water_distance = np.nan
    return truck_distance,water_distance

# # get truck/water distance
# def get_distance(path):
#     try:
#         path = path.split("-")
#         df_dummy = pd.DataFrame({"link_id":path})
#         df_dummy["ind"] = True
#         df_dummy_truck = df_dummy.merge(df_truck,on=["link_id"],how="left")
#         truck_distance = df_dummy_truck["distance"].sum()
#         df_dummy_water = df_dummy.merge(df_water,on=["link_id"],how="left")
#         water_distance = df_dummy_water["distance"].sum()
#     except:
#         truck_distance = np.nan
#         water_distance = np.nan
#     print(".",end="")
#     return truck_distance,water_distance

# def get_distance(path):
#     try:
#         path = path.split("-")
#         ind = df_truck["link_id"].isin(path)
#         truck_distance = df_truck.loc[ind,"distance"].sum()        
#         ind = df_water["link_id"].isin(path)
#         water_distance = df_water.loc[ind,"distance"].sum()        
#     except:
#         truck_distance = np.nan
#         water_distance = np.nan
#     print(".",end="")
#     return truck_distance,water_distance


for inputfile in inputfile_list:
    print(inputfile)
    # =============================================================================
    # 1. OD pair summary
    # =============================================================================
    outputfile = inputfile.replace("routing_","summary_")
    df = pd.read_csv(intput_folder + inputfile)
    df["path"] = df["path_1"]+"-"+df["path_2"]+"-"+df["path_3"]
    df["hour"] = df["hour_1"]+df["hour_2"]+df["hour_3"]
    df["truck_hour"] = df["hour_1"]+df["hour_3"]
    df["water_hour"] = df["hour_2"]
    
    df["distance"] = df["distance_1"]+df["distance_2"]+df["distance_3"]
    df["truck_distance"] = df["distance_1"]+df["distance_3"]
    df["water_distance"] = df["distance_2"]
    
    
    # df[["truck_distance","water_distance"]] = df["path"].apply(lambda x: pd.Series(get_distance(x)))
    
    # convert to numbers
    # df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df['hour'] = pd.to_numeric(df['hour'], errors='coerce')
    df["avg_speed"] = df["distance"]/df["hour"]
    df["truck_avg_speed"] = df["truck_distance"]/df["truck_hour"]
    df["water_avg_speed"] = df["water_distance"]/df["water_hour"]
    df['truck_distance'] = pd.to_numeric(df['truck_distance'], errors='coerce')
    df['water_distance'] = pd.to_numeric(df['water_distance'], errors='coerce')
    
    ind = (df["water_distance"]==0)|(df["water_distance"].isnull())
    no_water_ratio = (df.loc[ind,"tons"].sum())/(df["tons"].sum())
    print(inputfile,no_water_ratio)
    
    # quick summary
    df_summary = quick_summary(df[["distance","hour","avg_speed","truck_distance","water_distance","truck_hour","water_hour","truck_avg_speed","water_avg_speed"]])
    df_summary.to_csv(output_folder+outputfile)
    
    # for col in ["hour","distance","avg_speed","truck_distance","water_distance"]:
    #     ind = df[col].isnull()
    #     outputfile_col = outputfile.replace(".csv",f"_{col}.csv")
    #     df.loc[ind].to_csv(output_folder+outputfile_col,index=False)
    