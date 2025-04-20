import pandas as pd
import numpy as np
import os

intput_folder = "output/13/"
output_folder = "output/21/"
inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "routing_" in e]

# inputfile_list = inputfile_list[:10]
df_out = pd.DataFrame()
for inputfile in inputfile_list:
    print(inputfile)
    df = pd.read_csv(intput_folder + inputfile)
    
    # df["path"] = df["path_1"]+"-"+df["path_2"]+"-"+df["path_3"]
    # df["hour"] = df["hour_1"]+df["hour_2"]+df["hour_3"]
    df["truck_hour"] = df["hour_1"]+df["hour_3"]
    df["water_hour"] = df["hour_2"]
    
    # df["distance"] = df["distance_1"]+df["distance_2"]+df["distance_3"]
    df["truck_distance"] = df["distance_1"]+df["distance_3"]
    df["water_distance"] = df["distance_2"]
    # convert to numbers
    # df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    # df['hour'] = pd.to_numeric(df['hour'], errors='coerce')
    # df["avg_speed"] = df["distance"]/df["hour"]
    # df["truck_avg_speed"] = df["truck_distance"]/df["truck_hour"]
    # df["water_avg_speed"] = df["water_distance"]/df["water_hour"]
    df['truck_hour'] = pd.to_numeric(df['truck_hour'], errors='coerce')
    df['water_hour'] = pd.to_numeric(df['water_hour'], errors='coerce')
    df['truck_distance'] = pd.to_numeric(df['truck_distance'], errors='coerce')
    df['water_distance'] = pd.to_numeric(df['water_distance'], errors='coerce')
    
    # ind = (df["water_distance"]==0)|(df["water_distance"].isnull())
    # no_water_ratio = (df.loc[ind,"tons"].sum())/(df["tons"].sum())
    # print(inputfile,no_water_ratio)    
    
    # multiply assigned tons so that it can be calculated as sum. - later to be average
    for col in ["truck_hour","water_hour","truck_distance","water_distance"]:
        df[col] = df[col] * df['assigned_tons']
    
    # quick summary
    df = df.groupby(['ST_O', 'ST_D', 'FIPS_O', 'FIPS_D'],as_index=False)[["assigned_tons","truck_hour","water_hour","truck_distance","water_distance"]].sum()
    df_out = pd.concat([df_out,df])
    df_out = df_out.groupby(['ST_O', 'ST_D', 'FIPS_O', 'FIPS_D'],as_index=False)[["assigned_tons","truck_hour","water_hour","truck_distance","water_distance"]].sum()
    

# convert back to average
for col in ["truck_hour","water_hour","truck_distance","water_distance"]:
    df_out[col] = df_out[col] / df_out['assigned_tons']
df_out.to_csv(output_folder+"water_skim.csv", index=False)
