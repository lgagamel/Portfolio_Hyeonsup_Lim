import pandas as pd
from datetime import timedelta
import os
import math

output_folder = 'output/16/16_3/'  # Set the output directory for CSVs
os.makedirs(output_folder, exist_ok=True)


# Parameters
STOP_TIME_THRESHOLD = timedelta(minutes=120)  # Define stop time threshold
BEGIN_TIME_THRESHOLD = timedelta(minutes=10)
STOP_SPEED_THRESHOLD = 0.5  # Define speed below which vessel is considered stopped

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Radius of the Earth in miles
    R = 3958.8
    
    # Differences between the latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in miles
    distance = R * c
    return distance

def detect_stops_and_assign_od(data):
    # Ensure 'timestamp' is datetime and sort by MMSI and timestamp
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.sort_values(by=['MMSI', 'timestamp'])
    data["stop"] = 0
    ind = data["speed"]<=STOP_SPEED_THRESHOLD
    data.loc[ind,"stop"] = 1
    
    # Initialize variables
    od_data = []
    current_trip = None
    last_stop_time = None
    current_od_id = 0
    

    # Iterate over each vessel's data
    for MMSI, vessel_data in data.groupby('MMSI'):
        current_trip = None
        last_begin_time = None
        last_stop_time = None
        current_od_id = 0

        # Iterate over each row of the vessel's data
        prev_stop = 0
        prev_lat = 0
        prev_lon = 0
        for i, row in vessel_data.iterrows():
            current_stop = row['stop']
            timestamp = row['timestamp']
            lat, lon = row['lat'], row['lon']
            
            if (current_stop==0)&(prev_stop==1):
                if last_stop_time is not None:
                    if (timestamp - last_stop_time >= STOP_TIME_THRESHOLD):
                        current_trip = {
                            'MMSI': MMSI,
                            'start_lat': lat,
                            'start_lon': lon,
                            'start_time': timestamp
                        }
                        last_stop_time = None
                        last_begin_time = timestamp
                        prev_lat, prev_lon = lat, lon
                    else:
                        last_stop_time = None
            elif (current_stop==1)&(prev_stop==0):
                if last_stop_time is None:
                    last_stop_time = timestamp
                if last_begin_time is not None:
                    if haversine_distance(prev_lat, prev_lon, lat, lon)>10:
                        if (current_trip is not None)&(timestamp - last_begin_time >= BEGIN_TIME_THRESHOLD):
                            # Complete the trip
                            current_trip['end_lat'] = lat
                            current_trip['end_lon'] = lon
                            current_trip['end_time'] = timestamp
                            current_trip['od_id'] = current_od_id
                            current_od_id += 1
                            od_data.append(current_trip)
                            current_trip = None
                            last_begin_time = None
                    
                # current_trip = {
                #     'MMSI': MMSI,
                #     'end_lat': lat,
                #     'end_lon': lon,
                #     'end_time': timestamp
                # }
                # od_data.append(current_trip)
            else:
                pass 
            prev_stop = current_stop
    return pd.DataFrame(od_data)

inputfile_list = os.listdir('output/16/16_2/')

for inputfile in inputfile_list:
    print(inputfile)
    # Load the AIS data
    MMSI = int(inputfile.replace(".csv",""))
    # data = pd.read_csv('/path/to/your/ais_data.csv')
    data = pd.read_csv(f'output/16/16_2/{MMSI}.csv')
    data = data.rename(columns={"BaseDateTime":"timestamp",
                                "LAT":"lat",
                                "LON":"lon",
                                "SOG":"speed",
                                # "MMSI_NUMBER":"MMSI"
                                })
    
    
    # Detect stops and assign OD pairs
    od_data = detect_stops_and_assign_od(data)
    
    
    # Save the processed data with OD pairs
    od_data.to_csv(output_folder+f'OD_{MMSI}.csv', index=False)
    
