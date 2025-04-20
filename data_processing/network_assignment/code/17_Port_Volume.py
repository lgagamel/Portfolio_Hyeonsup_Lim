import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os
import numpy as np

intput_folder = "output/13/"
output_folder = "output/17/"
os.makedirs(output_folder, exist_ok=True)

inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "port_volume_" in e]


# =============================================================================
# 1. merge network and assigned volume
# =============================================================================
for inputfile in inputfile_list:    
    print(inputfile)
    # Load data
    df_obs = gpd.read_file("output/06/ports.shp")
    df_est = pd.read_csv(intput_folder+inputfile)
    # df_est = df_est.rename(columns={"link_id":"link_id_PW"})
    df_est["link_id_PW"] = df_est["node_id_p"].apply(lambda x: x.replace("P","PW"))
    
    outputfile = inputfile.replace("link_volume_","port_obs_vs_est_")
    outputfile = outputfile.replace(".csv",".png")
    
    ind = df_obs["TOTAL_impu"]==0
    df_obs = df_obs.loc[ind]
    df_obs["TOTAL"]
    df_obs["PORT"] = df_obs["PORT"].astype(int)
    df_obs = df_obs[["PORT","link_id_PW","TOTAL","geometry"]]
    df_obs = df_obs.dropna()
    
    df_est = df_est.rename(columns={"tons":"tons_est"})
    df_est = df_est[["link_id_PW","tons_est"]]
    
    df = df_obs.merge(df_est,on=["link_id_PW"],how="left")
    
    top_10_df = df.nlargest(10, 'TOTAL')
    top_10_df = top_10_df.sort_values(by='TOTAL', ascending=False)
    
    # Set the figure size
    plt.figure(figsize=(6, 3))
    
    # Create a bar chart with two bars for each index
    indices = top_10_df.index
    bar_width = 0.35
    # index = np.arange(len(indices))
    index = np.array(range(len(indices)))
    
    # Plot the first column
    plt.bar(index, top_10_df['TOTAL'], bar_width, label='Principal Port Volume', edgecolor="black")
    
    # Plot the second column, offset by the width of the bars
    plt.bar(index + bar_width, top_10_df['tons_est'], bar_width, label='Estimated Volume', edgecolor="black")
    
    # Add labels, title, and legend
    plt.xlabel('Rank # by Principal Port Volume')
    plt.ylabel('Tonnage')
    plt.title('Principal Port Volume vs Estimated Volume')
    plt.xticks(index + bar_width / 2, index+1, rotation=45)
    plt.legend()
    
    # Show the plot
    plt.tight_layout()
    # plt.grid(True)
    plt.savefig(output_folder+outputfile,dpi=300)
    plt.show()
    plt.close()    
    
    