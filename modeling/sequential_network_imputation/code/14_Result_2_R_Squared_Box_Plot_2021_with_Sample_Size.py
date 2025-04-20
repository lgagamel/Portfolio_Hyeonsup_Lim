import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df_out = pd.DataFrame()
# itr_n = [11,15]
year = "2021"
print(year)
# =============================================================================
# R-squared
# =============================================================================
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
df_out["value"]="R-squared"
# =============================================================================
# Sample size
# =============================================================================
df_sample_size_original = pd.read_csv("../01_TMAS_Data_Processing/output/1_volume_by_class_"+year+".csv")
df_sample_size = pd.DataFrame()
for col in target_measure_columns:
    df_tmp = df_sample_size_original[[col]].copy()
    df_tmp.columns = ["Avg. Sample Size"]
    df_tmp["class"] = col.split("_")[-1]
    df_tmp["year"] = year
    df_sample_size = pd.concat([df_sample_size,df_tmp])


df_sample_size = df_sample_size.groupby(["class"],as_index=False)["Avg. Sample Size"].mean()
df_sample_size["class_"] = df_sample_size["class"].astype(int)
df_sample_size = df_sample_size.sort_values(by="class_")

for template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
    print(template)
    fig = px.box(df_out, x="class", y="R-squared",color="value", template=template,width=800, height=400)
    fig.add_trace(
        go.Scatter(
            x=df_sample_size["class"],
            y=df_sample_size["Avg. Sample Size"],
            yaxis="y2",            
            name="Avg. Sample Size",
            marker=dict(color="crimson"),
        )
    )

    fig.update_layout(
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1),
        # showlegend=False,
        legend_title_text='',
        yaxis=dict(
            title=dict(text="R-squared"),
            side="left",            
            range=[0,1],
        ),
        yaxis2=dict(
            title=dict(text="Avg. Sample Size"),
            side="right",
            overlaying="y",
            tickmode="auto",
        ))

    # fig.write_html("output/step_12/"+template+".html")
    # fig.write_image("output/step_11/"+template+".png")
    fig.write_image("output/step_14/2021_"+template+".svg")
    fig.show()


