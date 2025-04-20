import os

folder_list = ["output"] + ["output/step_"+str(i+1) for i in range(14)]
folder_list = folder_list + ["output/step_2/shapefile",
                             "output/step_3/shapefile"]
for folder in folder_list:    
    try:
        os.mkdir(folder)        
    except:
        pass
