import pickle
import pandas as pd

output_folder = "output/23/"

# Load the dictionary from the pickle file
with open(output_folder + 'OD_by_link.pkl', 'rb') as f:
    OD_by_link = pickle.load(f)

link_list = ["W133822","W106002"]

for i,link in enumerate(link_list):
    df_out = pd.DataFrame([OD_by_link[link]]).T
    df_out = df_out.reset_index()
    df_out.columns = ["OD","assigned_tons"]
    df_out.to_csv(output_folder+f"{link}.csv", index=False)    
    if i>=10:
        break