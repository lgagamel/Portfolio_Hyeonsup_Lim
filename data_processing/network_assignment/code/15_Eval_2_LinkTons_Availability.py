import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import contextily as ctx

output_folder = "output/15/"

# Load the link layer shapefile
link_gdf = gpd.read_file('output/01/water_links.shp')
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
link_gdf["TOTAL"] = link_gdf["TOTALUP"]+link_gdf["TOTALDOWN"]

link_gdf["LinkTon_Reported"] = (~link_gdf["TOTAL"].isnull())
link_gdf["TOTAL"] = link_gdf["TOTAL"].fillna(0)
# link_gdf['line_width'] = link_gdf['TOTAL'].apply(lambda x: determine_line_width(x, df_width))
link_gdf['line_width'] = link_gdf['TOTAL'].apply(lambda x: min(5,max(0.1,x/10000000)))

# Merge the second dataframe with the link layer by 'X1'
# link_gdf = link_gdf.merge(df_style, on='GEO_CLASS', how='left')

# Plot the map with custom line width, color, and style
fig, ax = plt.subplots(figsize=(10, 6))


ind = link_gdf["LinkTon_Reported"]
# LinkTon_Reported==True
for idx, row in link_gdf.loc[ind].iterrows():    
    try:
        ax.plot(row['geometry'].xy[0], row['geometry'].xy[1],
                linewidth=row['line_width'],
                color="black",
                linestyle="-")
    except:
        pass

# LinkTon_Reported==False
for idx, row in link_gdf.loc[~ind].iterrows():    
    try:
        ax.plot(row['geometry'].xy[0], row['geometry'].xy[1],
                linewidth=1,
                color="red",
                linestyle="--")
    except:
        pass
    
# Optional: Create a custom legend
legend_elements = [Line2D([0], [0], color='black', lw=0.1, linestyle='-', label='<=1M Tons'),
                   Line2D([0], [0], color='black', lw=1, linestyle='-', label='10M Tons'),
                   Line2D([0], [0], color='black', lw=5, linestyle='-', label='>=500M Tons'),
                   Line2D([0], [0], color='red', lw=2, linestyle='--', label='Link Ton Not Reported')]
ax.legend(handles=legend_elements, loc='upper right')

# Set the title and show the plot
# ax.set_title('Custom Styled Map Based on Dataframe Inputs')
plt.xlim([-1.45e7, -7.50e6])
plt.ylim([2.85e6, 6.40e6])
ax.set_xticks([])
ax.set_yticks([])
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=5)
plt.savefig(output_folder+"USACE_link_tons.png",dpi=300)
plt.show()
plt.close()
