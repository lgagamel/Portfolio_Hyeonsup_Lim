import pandas as pd
import pickle
import os

intput_folder = "output/13/"
output_folder = "output/23/"
inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "routing_" in e]

# inputfile_list = inputfile_list[:2]
OD_by_link = {}
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
        path = row["path"].split("-")
        for link in path:
            if len(link)>0:
                if link not in OD_by_link:
                    OD_by_link[link] = {}
                try:
                    OD_by_link[link][row["OD"]] = OD_by_link[link][row["OD"]] + row["assigned_tons"]
                except:
                    OD_by_link[link][row["OD"]] = row["assigned_tons"]
                
# Save the dictionary to a pickle file
with open(output_folder+'OD_by_link.pkl', 'wb') as f:
    pickle.dump(OD_by_link, f)


for i,link in enumerate(OD_by_link):
    df_out = pd.DataFrame([OD_by_link[link]]).T
    df_out = df_out.reset_index()
    df_out.columns = ["OD","assigned_tons"]
    df_out.to_csv(output_folder+f"{link}.csv", index=False)    
    if i>=10:
        break
    
