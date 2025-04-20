import os
import pandas as pd
import csv

# Path to directory containing AIS data files
data_dir = 'output/16/16_1/'  # Set the path where your data files are stored
output_folder = 'output/16/16_2/'  # Set the output directory for CSVs

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to process and save data by IMO number
def process_ais_data(file_path, output_folder):
    df = pd.read_csv(file_path)
    ind = df["MMSI"].isnull()
    df = df.loc[~ind]
    df["MMSI"] = df["MMSI"].astype(int)
    for MMSI, group in df.groupby('MMSI'):
        # print(imo)
        if pd.isnull(MMSI):  # Skip rows with missing IMO numbers
            continue
        # Define the CSV file name for this IMO number
        output_file = os.path.join(output_folder, f'{MMSI}.csv')

        # Append data to the IMO-specific CSV file
        if not os.path.exists(output_file):
            group.to_csv(output_file, mode='w', header=True, index=False)
        else:
            group.to_csv(output_file, mode='a', header=False, index=False)

# Loop through all AIS files in the directory and process them
for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):  # Adjust if your files are not CSVs
        file_path = os.path.join(data_dir, filename)
        print(f"Processing {filename}")
        process_ais_data(file_path, output_folder)

print("AIS data processing complete.")
