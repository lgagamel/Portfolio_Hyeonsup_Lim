import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import contextily as ctx
import os

intput_folder = "output/13/"
output_folder = "output/15/"
inputfile_list = os.listdir(intput_folder)
inputfile_list = [e for e in inputfile_list if "water_link_volume_" in e]

for inputfile in inputfile_list:    
    print(inputfile)
    # Load the link layer shapefile
    link_gdf = gpd.read_file('output/01/water_links.shp')
    df_est = pd.read_csv(intput_folder+inputfile)
    outputfile = inputfile.replace("link_volume_","est_volume_")
    outputfile = outputfile.replace(".csv",".png")
    print(outputfile)
    
    df_est = df_est.rename(columns={"tons":"tons_est"})
    df_est = df_est[["link_id","tons_est"]]

    link_gdf = link_gdf.merge(df_est,on=["link_id"],how="left")

    
    # target_CRS = 'EPSG:4326'
    target_CRS = 'EPSG:3857'
    link_gdf = link_gdf.to_crs(target_CRS)
    
    # Load the dataframes
    df_width = pd.read_csv('../../__INPUT__/Graph/water_links_width.csv')
    df_style = pd.read_csv('../../__INPUT__/Graph/water_links_style.csv')
    
    # Function to determine line width based on value ranges
    def determine_line_width(value, df_width):
        for idx, row in df_width.iterrows():
            if row['min_value'] <= value < row['max_value']:
                return row['line_width']
        return df_width['line_width'].max()  # Default line width if no range is matched
    
    # Assume the shapefile has a column 'value' that we'll use to determine line width
    # link_gdf["TOTAL"] = link_gdf["TOTALUP"]+link_gdf["TOTALDOWN"]
    
    # link_gdf["LinkTon_Reported"] = (~link_gdf["TOTAL"].isnull())
    link_gdf["tons_est"] = link_gdf["tons_est"].fillna(0)
    # link_gdf['line_width'] = link_gdf['TOTAL'].apply(lambda x: determine_line_width(x, df_width))
    link_gdf['line_width'] = link_gdf['tons_est'].apply(lambda x: min(5,max(0.1,x/10000000)))
    
    # Merge the second dataframe with the link layer by 'X1'
    # link_gdf = link_gdf.merge(df_style, on='GEO_CLASS', how='left')
    
    # Plot the map with custom line width, color, and style
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    # LinkTon_Reported==True
    for idx, row in link_gdf.iterrows():    
        try:
            ax.plot(row['geometry'].xy[0], row['geometry'].xy[1],
                    linewidth=row['line_width'],
                    color="blue",
                    linestyle="-")
        except:
            pass
    
        
    # Optional: Create a custom legend
    legend_elements = [Line2D([0], [0], color='blue', lw=0.1, linestyle='-', label='<=1M Tons Est.'),
                       Line2D([0], [0], color='blue', lw=1, linestyle='-', label='10M Tons Est.'),
                       Line2D([0], [0], color='blue', lw=5, linestyle='-', label='>=50M Tons Est.')]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Set the title and show the plot
    # ax.set_title('Custom Styled Map Based on Dataframe Inputs')
    plt.xlim([-1.45e7, -7.50e6])
    plt.ylim([2.85e6, 6.40e6])
    ax.set_xticks([])
    ax.set_yticks([])
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=5)
    plt.savefig(output_folder+outputfile,dpi=300)
    plt.show()
    plt.close()    
