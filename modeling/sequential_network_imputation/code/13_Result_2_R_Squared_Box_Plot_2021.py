import pandas as pd
import plotly.express as px



df_out = pd.DataFrame()
# itr_n = [11,15]
for i,year in enumerate(["2021"]):
    print(year)
    df = pd.read_csv("output/step_10/"+year+"/summary.csv")
    target_measure_columns = list(df.columns)[df.columns.get_loc("cls_5"):df.columns.get_loc("cls_13")+1]
    df_grp = df.groupby(["random_seed"],as_index=False)["itr"].max()
    df_grp = df_grp.rename(columns={"itr":"itr_max"})
    df = df.merge(df_grp,on=["random_seed"],how="left")
    df = df.loc[df["itr"]==df["itr_max"]]
    df = df.drop(columns=["itr_max"])
    for col in target_measure_columns:
        df_tmp = df[[col]].copy()
        df_tmp.columns = ["R-squared"]
        df_tmp["class"] = col.split("_")[-1]
        df_tmp["year"] = year
        df_out = pd.concat([df_out,df_tmp])


# layout_set = {}
layout_set = {"boxmode": "overlay", "showlegend":False,"yaxis":{"range":[0,1]}}
for template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
    print(template)
    fig = px.box(df_out, x="class", y="R-squared",color="year", template=template,width=800, height=400)
    fig.update_layout(layout_set)
    # fig.write_html("output/step_12/"+template+".html")
    # fig.write_image("output/step_11/"+template+".png")
    fig.write_image("output/step_13/2021_"+template+".svg")
    fig.show()


