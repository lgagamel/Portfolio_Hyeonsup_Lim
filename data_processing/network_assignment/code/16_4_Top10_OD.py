import pandas as pd
import os

output_folder = 'output/16/16_4/'  # Set the output directory for CSVs
os.makedirs(output_folder, exist_ok=True)

# =============================================================================
# top 50 county od
# =============================================================================
df_county_od = pd.read_csv("output/10/10_1/county_od.csv")
df_county_od = df_county_od.sort_values(by="Final",ascending=False)
df_county_od = df_county_od.iloc[:50]
df_county_od.to_csv(output_folder+"county_od_top.csv",index=False)




