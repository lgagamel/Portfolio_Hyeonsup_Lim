# =============================================================================
# Script Name : Gravity_Model_County_to_FAF.py
# Author      : Hyeonsup Lim, ORNL (limh@ornl.gov)
# Date        : 2025-03-05
# Description : Gravity model with IPF to estimate disaggregated-level (county) OD and calibrate/evaluate the model based on aggregated-level (FAF) OD
# Input : FAF OD ('input/faf_od_data.csv'), origin total ('input/county_origin_sum.csv'), destination total ('input/county_destination_sum.csv'), county-to-FAF mapping ('input/county_mapping.csv'), county distance ('input/county_distance.csv')
# Output : Estimated OD ('output/final_county_od.csv')
# =============================================================================


import numpy as np
import pandas as pd
from scipy.optimize import minimize
from ipfn import ipfn
import matplotlib.pyplot as plt
import os

os.makedirs("output/",exist_ok=True)


# =============================================================================
# Load input data
# =============================================================================
# Load Data from CSV
faf_od_data = pd.read_csv("input/faf_od_data.csv")
county_mapping = pd.read_csv("input/county_mapping.csv")
county_origin_sum = pd.read_csv("input/county_origin_sum.csv")
county_destination_sum = pd.read_csv("input/county_destination_sum.csv")
county_distance_df = pd.read_csv("input/county_distance.csv")

# Merge data to form the initial county OD dataframe
county_od_df = county_distance_df.merge(county_origin_sum, on='origin')
county_od_df = county_od_df.merge(county_destination_sum, on='destination')
county_od_df['total'] = county_od_df['total_x'] * county_od_df['total_y']
county_od_df = county_od_df.drop(columns=['total_x', 'total_y'])

# Add origin_FAF and destination_FAF by merging with county mapping
county_od_df = county_od_df.merge(county_mapping.rename(columns={'county': 'origin'}), on='origin')
county_od_df = county_od_df.merge(county_mapping.rename(columns={'county': 'destination', 'FAF': 'destination_FAF'}), on='destination')
county_od_df.rename(columns={'FAF': 'origin_FAF'}, inplace=True)


# =============================================================================
# functions: gravity, IPF, minimization objective
# =============================================================================
# Gravity Model
def gravity_model(beta):
    county_od_df['total'] *= 1/(county_od_df['distance']**beta)
    return county_od_df

# IPF used for training (without considering FAF OD)
def apply_ipf_train(beta):
    county_od_df_adj = gravity_model(beta).copy()
    aggregates = [
        county_origin_sum.groupby(['origin'])['total'].sum(),
        county_destination_sum.groupby(['destination'])['total'].sum(),
    ]
    dimensions = [['origin'], ['destination']]
    
    IPF = ipfn.ipfn(county_od_df_adj, aggregates, dimensions)
    return IPF.iteration()

# IPF used for final estimation (with considering FAF OD)
def apply_ipf_final(beta):
    county_od_df_adj = gravity_model(beta).copy()
    aggregates = [        
        county_origin_sum.groupby(['origin'])['total'].sum(),
        county_destination_sum.groupby(['destination'])['total'].sum(),
        faf_od_data.groupby(['origin_FAF', 'destination_FAF'])['total'].sum(),
    ]
    dimensions = [['origin'], ['destination'],['origin_FAF', 'destination_FAF']]
    IPF = ipfn.ipfn(county_od_df_adj, aggregates, dimensions)
    return IPF.iteration()

# Objective Function for Optimization
performance_data = []
def objective(beta):
    county_od_adjusted = apply_ipf_train(beta)
    aggregated_faf_od = county_od_adjusted.groupby(['origin_FAF', 'destination_FAF'])['total'].sum().reset_index()
    merged_faf_od = faf_od_data.merge(aggregated_faf_od, on=['origin_FAF', 'destination_FAF'], how='outer', suffixes=('_observed', '_estimated')).fillna(0)
    error = np.mean(np.abs(merged_faf_od['total_observed'] - merged_faf_od['total_estimated']))
    performance_data.append((beta[0], error))
    return error

# =============================================================================
# Optimize Beta
# =============================================================================
result = minimize(objective, x0=[0.1], bounds=[(0, 2)], method='L-BFGS-B', options={'maxiter': 20, 'disp': True, 'ftol': 1e-10})
optimal_beta = result.x[0]
print(f"Optimal beta for gravity model: {optimal_beta}")

# =============================================================================
# Save performance data
# =============================================================================
performance_df = pd.DataFrame(performance_data, columns=['beta', 'error'])
performance_df = performance_df.sort_values(by=["beta"])
performance_df.to_csv("output/performance_data.csv", index=False)

# Plot performance data
plt.figure(figsize=(8, 5))
plt.plot(performance_df['beta'], performance_df['error'], marker='o', linestyle='-')
plt.xlabel('Beta')
plt.ylabel('Error')
plt.title('Model Performance by Beta Values')
plt.grid(True)
plt.savefig("output/performance_plot.svg")
plt.show()


# =============================================================================
# output
# =============================================================================
# Get final county-level OD
final_county_od = apply_ipf_final(optimal_beta)
final_county_od.to_csv("output/final_county_od.csv", index=False)

# =============================================================================
# check
# =============================================================================
final_county_od.groupby(['origin'])['total'].sum().to_csv("output/county_origin_sum_check.csv")
final_county_od.groupby(['destination'])['total'].sum().to_csv("output/county_destination_sum_check.csv")
final_county_od.groupby(['origin_FAF', 'destination_FAF'])['total'].sum().to_csv("output/faf_od_data_check.csv")

