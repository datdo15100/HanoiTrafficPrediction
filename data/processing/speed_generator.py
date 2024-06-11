import pickle
import pandas as pd
import geopandas as gpd

# Load the network DBF file
network_dbf_path = '../hanoi/network.dbf'
network_df = gpd.read_file(network_dbf_path)

# Extract unique IDs from the network DBF
network_ids = network_df['Id'].unique()

# Initialize a DataFrame to hold the average speed for each ID
speed_data = pd.DataFrame(columns=network_ids, index=[0])
speed_data = speed_data.astype(float)  # Ensure the DataFrame columns are of numeric type

# Load the saved dataframes from the pickle file
SAVE_FILE = "../hanoi/all_dataframes_final.pkl"

with open(SAVE_FILE, 'rb') as f:
    loaded_dataframes = pickle.load(f)

current_folder = 4383493
days = 19

for day in range(days):
    folder = loaded_dataframes[current_folder]
    for dataframe in folder.values():
        dataframe.columns = list(map(lambda x: x.split('_')[1], dataframe.columns))
        if 'HvgSp' in dataframe.columns:
            temp_df = pd.DataFrame([dataframe['HvgSp']], columns=dataframe.Id)
            temp_df = temp_df.reindex(columns=speed_data.columns, fill_value=0)
            speed_data = pd.concat([speed_data, temp_df], ignore_index=True)
    
    current_folder += 1
    
# Remove completely empty rows
speed_data.dropna(how='all', inplace=True)
# Perform linear interpolation to fill in missing values
data_interpolated = speed_data.interpolate(method='linear', axis=1)

print(data_interpolated.head())
print(data_interpolated.shape)

# Save the interpolated data to a CSV file
data_interpolated.to_csv('../hn_speed.csv', index=False)
