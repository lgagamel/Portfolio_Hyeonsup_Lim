import pandas as pd
import plotly.express as px


df = pd.read_csv("output/step_10/summary.csv")
# df = pd.read_csv("output/step_10/12.csv")

df_grp = df.groupby(["random_seed"],as_index=False)["itr"].max()
df_grp = df_grp.rename(columns={"itr":"itr_max"})
df = df.merge(df_grp,on=["random_seed"],how="left")
df = df.loc[df["itr"]==df["itr_max"]]
df = df.drop(columns=["itr_max"])

target_measure_columns = list(df.columns)[df.columns.get_loc("cls_5"):]
df_out = pd.DataFrame()
for col in target_measure_columns:
    print(col)
    df_tmp = df[[col]].copy()
    df_tmp.columns = ["R-squared"]
    df_tmp["class"] = col.split("_")[-1]
    df_out = pd.concat([df_out,df_tmp])


layout_set = {"boxmode": "overlay", "showlegend":False}
for template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
    print(template)
    fig = px.box(df_out, x="class", y="R-squared",color="class", points="all",template=template,width=800, height=400)
    fig.update_layout(layout_set)
    fig.write_html("output/step_11/"+template+".html")
    # fig.write_image("output/step_11/"+template+".png")
    # fig.write_image("output/step_11/"+template+".svg")
    fig.show()


