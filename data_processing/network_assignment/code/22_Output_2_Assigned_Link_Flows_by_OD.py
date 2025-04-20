import pandas as pd
import pickle
import os

intput_folder = "output/13/"
output_folder = "output/22/"
inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "routing_" in e]

# inputfile_list = inputfile_list[:2]
link_flow_by_OD = {}
for inputfile in inputfile_list:
    df = pd.read_csv(intput_folder + inputfile)
    df["path_1"] = df["path_1"].fillna("")
    df["path_2"] = df["path_2"].fillna("")
    df["path_3"] = df["path_3"].fillna("")
    
    df["path"] = df["path_1"]+"-"+df["path_2"]+"-"+df["path_3"]
    ind = df["path"].apply(lambda x: len(x)<=2)
    print(inputfile, sum(ind))
    df = df.loc[~ind]
    
    df["FIPS_O"] = df["FIPS_O"].apply(lambda x: str(int(x)).zfill(5))
    df["FIPS_D"] = df["FIPS_D"].apply(lambda x: str(int(x)).zfill(5))
    df["OD"] = df["FIPS_O"] + "-" + df["FIPS_D"]    
    
    for i,row in df.iterrows():
        if row["OD"] not in link_flow_by_OD:
            link_flow_by_OD[row["OD"]] = {}
            
        path = row["path"].split("-")
        for link in path:
            if len(link)>0:
                try:
                    link_flow_by_OD[row["OD"]][link] = link_flow_by_OD[row["OD"]][link] + row["assigned_tons"]
                except:
                    link_flow_by_OD[row["OD"]][link] = row["assigned_tons"]
                
# Save the dictionary to a pickle file
with open(output_folder+'link_flow_by_OD.pkl', 'wb') as f:
    pickle.dump(link_flow_by_OD, f)


df_top_od = pd.read_csv("output/20/top_od.csv")

for i,OD in enumerate(list(df_top_od["OD"])):
    df_out = pd.DataFrame([link_flow_by_OD[OD]]).T
    df_out = df_out.reset_index()
    df_out.columns = ["link","assigned_tons"]
    df_out.to_csv(output_folder+f"{OD}.csv", index=False)    
    if i>=10:
        break
    
