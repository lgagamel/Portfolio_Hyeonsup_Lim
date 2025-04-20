import geopandas as gpd
import os
import sys
import json
import pandas as pd
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
#p4_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis\P3_VMT\p4.shp'
p4_fp1 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Reference\20170412_TerminalFuelConsumption\20170412_TerminalFuelConsumption\PetroleumProduct_Terminals_US_EIA\PetroleumProduct_Terminals_Polygon_FuelConsumption.shp'
p4_fp2 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Reference\20170412_TerminalFuelConsumption\20170412_TerminalFuelConsumption\PetroleumProduct_Terminals_US_EIA\PetroleumProduct_Terminals_US_201608.shp'
out_fp1 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis\P4_Consumption\test.json'
out_fp2 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis\P4_Consumption\test.html'

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

fig = go.Figure(go.Choroplethmapbox(geojson=j_file,locations=p4_1.FID_1, 
#                                    z=p4_1.Sum_VMT12,
                                    z=0*p4_1.Sum_VMT12,
                                    colorscale="viridis", 
                                    #zmin=min(p4_1.Sum_VMT12), zmax=max(p4_1.Sum_VMT12),
                                    zmin=0, zmax=1000,
                                    marker_opacity=0.1, marker_line_width=1, marker_line_color='black'))


#fig = go.Figure(go.Choroplethmapbox(geojson=j_file, locations=df.fips, z=df.unemp,
#                                    colorscale="Viridis", zmin=0, zmax=12,
#                                    marker_opacity=0.5, marker_line_width=0))
fig.add_trace(go.Scattermapbox(
        lat=p4_2['Latitude'],
        lon=p4_2['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=p4_2['State']+'<br>'+p4_2['Company']+'<br>'+(round(p4_1['Sum_VMT12'])).astype(str),
    ))
#fig.add_trace(            
#        go.Scattergeo(            
#            visible=True,
##            locationmode = 'USA-states',
#            lon = p4_2['Longitude'],
#            lat = p4_2['Latitude'],
#            text = p4_2['State']+'<br>'+p4_2['Company']+'<br>'+str(round(p4_1['Sum_VMT12'])),
#            marker = dict(
#                autocolorscale=False,                 
#                size = p4_1['Sum_VMT12']/float(p4_1['Sum_VMT12'].mean())*30,
#                #cmin = 0,
#                #cmax = 1,
#                #color = 'rgb(0,0,0)',
#                line_color='rgb(40,40,40)',
#                #colorscale='Magma',
#                line_width=0.5,
#                sizemode = 'area',
#                showscale = True
#            ),
#            name = 'test'))
#            
fig.update_layout(mapbox_style="open-street-map",geo_scope='usa',
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})


            
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html(out_fp2, auto_open=True)
