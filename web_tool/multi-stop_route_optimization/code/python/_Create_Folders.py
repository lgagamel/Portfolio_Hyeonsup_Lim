import os

folder_list = ["output"] + ["output/"+str(i+1).zfill(2) for i in range(5)]
folder_list = folder_list + ["log"]
folder_list = folder_list + ["output/_temp"]
folder_list = folder_list + ["output/_temp/_images"]
# folder_list = folder_list + ["network/_network_original"]
# folder_list = folder_list + ["network/_network_simple"]
# folder_list = folder_list + ["network/_address"]
# folder_list = folder_list + ["network/_shp"]
# folder_list = folder_list + ["network/_network_simple_entire"]
# folder_list = folder_list + ["network/_us_center_point_list"]
# folder_list = folder_list + ["network/_network_simple_edges"]
# folder_list = folder_list + ["network/_network_simple_nodes"]
# folder_list = folder_list + ["network/_network_simple_dist"]



for folder in folder_list:    
    try:
        os.mkdir(folder)        
    except:
        pass

# with open("output/_address/address_xy.csv", "w") as f:
#     f.write("address,x,y\n")

