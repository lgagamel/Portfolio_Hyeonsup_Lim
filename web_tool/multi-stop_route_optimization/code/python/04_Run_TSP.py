# https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847
import six
import sys
sys.modules['sklearn.externals.six'] = six

import pickle
import mlrose
# import numpy as np
# import networkx as nx
# import osmnx as ox
import pandas as pd
import time
import HL_TSP

# =============================================================================
# load input
# =============================================================================
df_xy = pd.read_csv("output/01/xy.csv")
df_xy = df_xy.dropna()

# get a graph
with open("output/03/node_list.pkl", 'rb') as f:
    node_list = pickle.load(f)
    
with open("output/03/dist_array.pkl", 'rb') as f:
    dist_array = pickle.load(f)

with open("output/00/CheckBox_Open_TSP.txt", 'r') as f:
    CheckBox_Open_TSP = f.read()
    
if CheckBox_Open_TSP=="False":
    dist_array[:, 0] = 0 # onlt for open TSM

# =============================================================================
# model
# =============================================================================
best_state = HL_TSP.tsp_main(dist_array)
if CheckBox_Open_TSP=="True":
    best_state = best_state + [0]



# =============================================================================
# write coordinates and links
# =============================================================================
link = "https://www.google.com/maps/dir/"
N = 0
f_link = open("output/04/final.txt","w")
link_i = 0
f_coordinate = open("output/04/"+str(link_i)+".csv","w")
f_coordinate.write("original_i,original_address,y,x\n")

start = time.time()
for i,n in enumerate(best_state):
    end = time.time()
    elapsed_time = end - start
    if elapsed_time>1000:
        raise("taking too long 4")
        
    N = N + 1
    x = df_xy.iloc[n]["x"]
    y = df_xy.iloc[n]["y"]
    original_i = df_xy.iloc[n]["i"]
    original_address = df_xy.iloc[n]["address"]
    x = round(x,6)
    y = round(y,6)
    # coordinate = str(i) + "," + str(y) + "," + str(x)
    coordinate = str(y) + "," + str(x)
    tmp_str = str(original_i+1) + ',"' + original_address + '",' + coordinate
    f_coordinate.write(tmp_str+"\n")
    link = link + "/" + coordinate
    if N>=9:
        print(link)
        f_link.write(link+"\n")
        link = "https://www.google.com/maps/dir/"
        # link = link + "/" + coordinate
        N = 0
        f_coordinate.close()
        link_i= link_i + 1
        if n<(len(best_state)-1):
            f_coordinate = open("output/04/"+str(link_i)+".csv","w")
            f_coordinate.write("original_i,original_address,y,x\n")            
            # f_coordinate.write(tmp_str+"\n")
if N>0:
    print(link)
    f_link.write(link+"\n")
f_link.close()
f_coordinate.close()
