import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import contextily as ctx
import os
import pickle

output_folder = "output/22/"

# Load the link layer shapefile
gdf_water_original = gpd.read_file('output/01/water_links.shp')
gdf_truck_original = gpd.read_file('output/01/truck_links.shp')

# target_CRS = 'EPSG:4326'
target_CRS = 'EPSG:3857'
gdf_water_original = gdf_water_original.to_crs(target_CRS)
gdf_truck_original = gdf_truck_original.to_crs(target_CRS)



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
    


# OD = "27137-18089"
while True:
    gdf_water = gdf_water_original.copy()
    gdf_truck = gdf_truck_original.copy()
    try:
        OD,background_map_ind = input("OD:").split(" ")
        inputfile = output_folder + f"{OD}.csv"
        
        
        # df_est = pd.read_csv(inputfile)
        # df_est = df_est.rename(columns={"assigned_tons":"tons_est",
        #                                 "link":"link_id",
        #                                 })
        # df_est = df_est[["link_id","tons_est"]]
        
        df_est = pd.DataFrame([link_flow_by_OD[OD]]).T
        df_est = df_est.reset_index()
        df_est.columns = ["link_id","tons_est"]
        df_est.to_csv(output_folder+f"{OD}.csv", index=False)
        
        outputfile = f"{OD}.png"
        
        
        
        gdf_water = gdf_water.merge(df_est,on=["link_id"],how="left")
        gdf_truck = gdf_truck.merge(df_est,on=["link_id"],how="left")
        
        
        
        
        gdf_water = gdf_water.loc[gdf_water["tons_est"]>0]
        gdf_water['line_width'] = gdf_water['tons_est'].apply(lambda x: min(5,max(0.1,x/100000)))
        
        gdf_truck = gdf_truck.loc[gdf_truck["tons_est"]>0]
        gdf_truck['line_width'] = gdf_truck['tons_est'].apply(lambda x: min(5,max(0.1,x/100000)))
        
        
        # Plot the map with custom line width, color, and style
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        # LinkTon_Reported==True
        for idx, row in gdf_water.iterrows():    
            try:
                ax.plot(row['geometry'].xy[0], row['geometry'].xy[1],
                        linewidth=row['line_width'],
                        color="blue",
                        linestyle="-")
            except:
                pass
        
        for idx, row in gdf_truck.iterrows():    
            try:
                ax.plot(row['geometry'].xy[0], row['geometry'].xy[1],
                        linewidth=row['line_width'],
                        color="black",
                        linestyle="-")
            except:
                pass
            
            
        # Optional: Create a custom legend
        legend_elements = [
        Line2D([0], [0], color='blue', lw=0.1, linestyle='-', label='Water <=0.01M Tons Est.'),
        Line2D([0], [0], color='blue', lw=1, linestyle='-', label='Water 0.1M Tons Est.'),
        Line2D([0], [0], color='blue', lw=5, linestyle='-', label='Water >=0.5M Tons Est.'),
        Line2D([0], [0], color='black', lw=0.1, linestyle='-', label='Truck <=0.01M Tons Est.'),
        Line2D([0], [0], color='black', lw=1, linestyle='-', label='Truck 0.1M Tons Est.'),
        Line2D([0], [0], color='black', lw=5, linestyle='-', label='Truck >=0.5M Tons Est.')]
        # ax.legend(handles=legend_elements, loc='upper right')
        ax.legend(handles=legend_elements, loc='lower left')
        
        # Set the title and show the plot
        # ax.set_title('Custom Styled Map Based on Dataframe Inputs')
        # plt.xlim([-1.45e7, -7.50e6])
        # plt.ylim([2.85e6, 6.40e6])
        ax.set_xticks([])
        ax.set_yticks([])
        if background_map_ind=="yes":
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=5)
        plt.savefig(output_folder+outputfile,dpi=300)
        plt.show()
        plt.close()
    except:
        print("something got wrong.")
