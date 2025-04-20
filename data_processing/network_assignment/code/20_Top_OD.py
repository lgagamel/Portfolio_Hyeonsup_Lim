import pandas as pd

output_folder = "output/20/"
df = pd.read_csv("output/10/10_1/county_od.csv")
df["FIPS_O"] = df["FIPS_O"].apply(lambda x: str(int(x)).zfill(5))
df["FIPS_D"] = df["FIPS_D"].apply(lambda x: str(int(x)).zfill(5))
df["OD"] = df["FIPS_O"] + "-" + df["FIPS_D"]    

df = df.groupby(["OD"],as_index=False)["final"].sum()
df = df.sort_values(by="final",ascending=False)
df = df.iloc[:100]
df.to_csv(output_folder+"top_od.csv",index=False)