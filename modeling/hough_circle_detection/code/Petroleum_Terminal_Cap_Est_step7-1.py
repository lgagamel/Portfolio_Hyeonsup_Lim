import geopandas as gpd
import os
import sys
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
sys.path.append(r"C:\Users\9hl\Dropbox\ORNL\12.Python\1.BasicTools\190516_GIS_Basic_Function")

# File paths
#p4_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P3_VMT\p4.shp'
p2_capacity_final_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P2_Voronoi\beta3\p2_capacity_final2.shp'
p4_summary_fp = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P4_Consumption\p4_summary.csv'
out_fp1 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P7_Output_Figures\test.json'
out_fp2 = r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P7_Output_Figures\test.html'

# Read files
p2_capacity_final = gpd.read_file(p2_capacity_final_fp)
p4_summary = pd.read_csv(p4_summary_fp)


def add_scatter(p4_summary, fig, tmp_row, tmp_col, x_col, y_col, tmp_name, tmp_visible=False,tmp_color='#33CFA5',tmp_line='solid'):    
    fig.add_trace(
        go.Scatter(x=list(p4_summary[x_col]),
                   y=list(p4_summary[y_col]),
                   name=tmp_name,
                   visible=tmp_visible,
                   line=dict(color=tmp_color, dash=tmp_line)),
        row=tmp_row, col=tmp_col)
        
def add_scattergeo(fig,p2_capacity_final, tmp_beta, tmp_row, tmp_col):
    n = 100
    tmp_beta_col = 'est_b_'+ str(int(tmp_beta*n))
    fig.add_trace(go.Scattergeo(
            visible=True,
            locationmode = 'USA-states',
            lon = p2_capacity_final['Longitude'],
            lat = p2_capacity_final['Latitude'],
            text = p2_capacity_final['State']+'<br>'+p2_capacity_final['Company']+'<br>'+(round(p2_capacity_final[tmp_beta_col])).astype(str),
            marker = dict(
                autocolorscale=False,                 
                size = p2_capacity_final[tmp_beta_col]/float(p2_capacity_final[tmp_beta_col].mean())*30,
                #cmin = 0,
                #cmax = 1,
                #color = 'rgb(0,0,0)',
                line_color='rgb(40,40,40)',
                #colorscale='Magma',
                line_width=0.5,
                sizemode = 'area',
                showscale = True
            ),
            name = 'test')
            ,row=tmp_row, col=tmp_col)

def add_beta_line(p4_summary, fig, tmp_beta, y_col, tmp_row, tmp_col, tmp_visible=True,tmp_color='#636363',tmp_line='solid'):
    tmp_p4_summary = p4_summary.loc[p4_summary['beta']==tmp_beta]
    tmp_y = tmp_p4_summary[y_col]
    fig.add_trace(
        go.Scatter(x=[tmp_beta, tmp_beta],
                   y=[0, tmp_y.iloc[0]],
                   textposition="top center",  
                   textfont=dict(family="sans serif",size=18,color="Blue"),
                   name='cv threshold',
                   visible=tmp_visible,
                   mode="lines+markers+text",
                   line=dict(color=tmp_color, dash=tmp_line)),
        row=tmp_row, col=tmp_col)
    
    print(0,tmp_y.iloc[0])
        
def plot_all(p4_summary, out_fp2):    
    # Initialize figure with subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scatter"},{"type": "scattergeo"}]])
    
    # scatter plot 
    add_scatter(p4_summary, fig, 1, 1, 'beta', 'r2_TFC', 'r2_TFC', tmp_visible=True,tmp_color='#33CFA5',tmp_line='solid')
    #add_scatter(p4_summary, fig, 1, 1, 'beta', 'r2_LFC', 'r2_LFC', tmp_visible=True,tmp_color='#33CFA5',tmp_line='dash')
    
    # add threshold bar & map plot for o/d by cv    
    for i in range(len(p4_summary)):
        tmp_beta = p4_summary.beta[i]
        add_beta_line(p4_summary, fig, tmp_beta, 'r2_TFC', 1, 1)
        add_scattergeo(fig,p2_capacity_final, tmp_beta, 1, 2)
        
    # Make 0-1 trace visible
    fig.data[0].visible = True
    fig.data[1].visible = True
    
    # Create and add slider
    steps = []    
    no_cv_thr = int(len(p4_summary))
    no_subplots = int((len(fig.data)-1)/no_cv_thr)    
    
    for i in range(no_cv_thr):
        tmp_beta=p4_summary.beta[i]
        step = dict(method="restyle", 
                    args=["visible", [False] * len(fig.data)], 
                    label=tmp_beta)
        step["args"][1][0] = True
        for j in range(no_subplots):        
            step["args"][1][j+i*no_subplots+1] = True  
            #print(i,j+i*no_subplots+1)
        steps.append(step)
    
    sliders = [dict(active=0, currentvalue={"prefix": "CV Threshold: "}, steps=steps)]
    
    fig.update_layout(title='title',
                      showlegend = True, 
                      geo = dict(scope = 'usa',landcolor = 'rgb(217, 217, 217)'),
                      sliders=sliders)
    
    #fig.update_xaxes(range=[0, 235])
    #fig.update_yaxes(range=[0, 1])    
    
    fig.write_html(out_fp2, auto_open=True)



plot_all(p4_summary, out_fp2)
