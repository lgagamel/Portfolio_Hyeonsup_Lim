import pandas as pd
import matplotlib.pyplot as plt
import os

intput_folder = "output/13/"
output_folder = "output/15/"
inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "water_link_volume_" in e]


# =============================================================================
# 1. merge network and assigned volume
# =============================================================================
output_all = []
for inputfile in inputfile_list:    
    print(inputfile)
    output = inputfile.replace("water_link_volume_","").replace(".csv","")
    output = output.split("_")
    
    # Load data
    df_obs = pd.read_csv("output/01/water_links.csv")
    df_est = pd.read_csv(intput_folder+inputfile)
    outputfile = inputfile.replace("link_volume_","obs_vs_est_")
    outputfile = outputfile.replace(".csv",".png")
    
    df_obs["TOTAL"] = df_obs["TOTALUP"] + df_obs["TOTALDOWN"]
    df_obs = df_obs[["link_id","TOTAL"]]
    df_obs = df_obs.dropna()
    df_obs = df_obs.loc[df_obs["TOTAL"]>0]
    
    df_est = df_est.rename(columns={"tons":"tons_est"})
    df_est = df_est[["link_id","tons_est"]]
    
    df = df_obs.merge(df_est,on=["link_id"],how="left")    
    
    
    
    
    
    
    
    # =============================================================================
    # 2. compare linktons
    # =============================================================================
    
    
    # =============================================================================
    # 3. display scatter plot and calculate r2
    # =============================================================================
    r_value = df['TOTAL'].corr(df['tons_est'])
    r_squared = r_value ** 2
    r_value = round(r_value,4)
    r_squared = round(r_squared,4)
    print(r_value,r_squared)
    
    output.append(str(r_value))
    output.append(str(r_squared))
    output_all.append(output)    
    
    # Create the scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df['TOTAL'], df['tons_est'], color='black', marker='o')
    
    # Add labels and title
    plt.xlabel('Reported Link Tons')
    plt.ylabel('Estimated Link Tons')
    plt.title(outputfile.replace(".png","  ") + f'{r_squared}')
    
    # Apply log scale to both axes
    # plt.xscale('log')
    # plt.yscale('log')
    
    # plt.xlim([0,10000000])
    # plt.ylim([0,10000000])
    
    # Show the plot
    plt.grid(True)
    plt.savefig(output_folder+outputfile,dpi=300)
    plt.show()
    plt.close()

df_out = pd.DataFrame(output_all,columns=["b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","r","r2"])
df_out.to_csv(output_folder+"summary.csv",index=False)