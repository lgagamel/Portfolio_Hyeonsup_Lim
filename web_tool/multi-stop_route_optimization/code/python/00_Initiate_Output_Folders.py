import os
import shutil

folder_list = ["output/"+str(i).zfill(2) for i in range(5+1)]

try:
    shutil.rmtree("output")
except:
    pass
    


folder_list = ["log"]+ ["output"] + ["output/"+str(i).zfill(2) for i in range(5+1)]
folder_list = folder_list + ["output/05/_images"]

for folder in folder_list:    
    try:
        os.mkdir(folder)        
    except:
        pass

