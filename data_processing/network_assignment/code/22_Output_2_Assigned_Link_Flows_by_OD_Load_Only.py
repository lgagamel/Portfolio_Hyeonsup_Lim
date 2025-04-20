import pickle
import pandas as pd

output_folder = "output/22/"

# Load the dictionary from the pickle file
with open(output_folder + 'link_flow_by_OD.pkl', 'rb') as f:
    link_flow_by_OD = pickle.load(f)


# OD_list = ["27137-18089","27137-18127"]

# for i,OD in enumerate(OD_list):
#     df_out = pd.DataFrame([link_flow_by_OD[OD]]).T
#     df_out = df_out.reset_index()
#     df_out.columns = ["link","assigned_tons"]
#     df_out.to_csv(output_folder+f"{OD}.csv", index=False)    
#     if i>=10:
#         break
    
while True:
    OD = input("OD:")
    df_out = pd.DataFrame([link_flow_by_OD[OD]]).T
    df_out = df_out.reset_index()
    df_out.columns = ["link","assigned_tons"]
    df_out.to_csv(output_folder+f"{OD}.csv", index=False)
    print(f"processing {OD} complete")