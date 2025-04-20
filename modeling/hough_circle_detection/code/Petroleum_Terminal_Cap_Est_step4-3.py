import geopandas as gpd
import os
import sys
import json
import pandas as pd
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
#p4_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P3_VMT\p4.shp'
p4_fp1 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Reference\20170412_TerminalFuelConsumption\20170412_TerminalFuelConsumption\PetroleumProduct_Terminals_US_EIA\PetroleumProduct_Terminals_Polygon_FuelConsumption.shp'
p4_fp2 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Reference\20170412_TerminalFuelConsumption\20170412_TerminalFuelConsumption\PetroleumProduct_Terminals_US_EIA\PetroleumProduct_Terminals_US_201608.shp'
out_fp1 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption\test.json'
out_fp2 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption\test.html'

# Read files
p4_1 = gpd.read_file(p4_fp1)
p4_2 = gpd.read_file(p4_fp2)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})


# convert to GeoJSON
p4_1.to_file(out_fp1, driver = "GeoJSON")

with open(out_fp1) as geofile:
    j_file = json.load(geofile)
    
i=1
for feature in j_file["features"]:
    feature['id'] = feature['properties']['FID_1']
    i += 1
    

import plotly.graph_objects as go

fig = go.Figure(go.Scattergeo(
            visible=True,
            locationmode = 'USA-states',
            lon = p4_2['Longitude'],
            lat = p4_2['Latitude'],
            text = p4_2['State']+'<br>'+p4_2['Company']+'<br>'+(round(p4_1['Sum_VMT12'])).astype(str),
            marker = dict(
                autocolorscale=False,                 
                size = p4_1['Sum_VMT12']/float(p4_1['Sum_VMT12'].mean())*30,
                #cmin = 0,
                #cmax = 1,
                #color = 'rgb(0,0,0)',
                line_color='rgb(40,40,40)',
                #colorscale='Magma',
                line_width=0.5,
                sizemode = 'area',
                showscale = True
            ),
            name = 'test'))
            

            
fig.update_layout(mapbox_style="carto-positron",geo_scope='usa',
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})


            
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html(out_fp2, auto_open=True)

