import pickle
import pandas as pd
import geopandas as gpd

# Load the network DBF file
network_dbf_path = '../hanoi/network.dbf'
network_df = gpd.read_file(network_dbf_path)

# Filter based on multiple FRCs
selected_frcs = [3, 4]  # Change this to the desired FRCs
network_df = network_df[network_df['FRC'].isin(selected_frcs)]

# Combine segments by StreetName
combined_network = network_df.dissolve(by='StreetName')

# Initialize a DataFrame to hold the average speed for each StreetName
speed_data = pd.DataFrame(columns=combined_network.index, index=[0])
speed_data = speed_data.astype(float)  # Ensure the DataFrame columns are of numeric type

# Load the saved dataframes from the pickle file
SAVE_FILE = "../hanoi/all_dataframes_final.pkl"

with open(SAVE_FILE, 'rb') as f:
    loaded_dataframes = pickle.load(f)

# Iterate through each DataFrame in the dictionary and process the speed data
for key, dataframe in loaded_dataframes.items():
    # Standardize column names by stripping the prefix
    standardized_columns = {col: col.split('_')[1] for col in dataframe.columns if '_' in col}
    dataframe.rename(columns=standardized_columns, inplace=True)
    
    if 'HvgSp' in dataframe.columns and 'Id' in dataframe.columns:
        temp_df = pd.DataFrame([dataframe['HvgSp']], columns=dataframe['Id'])
        temp_df = temp_df.reindex(columns=network_df['Id'], fill_value=0)
        temp_df.columns = network_df.set_index('Id').loc[temp_df.columns, 'StreetName'].values
        temp_df = temp_df.T.groupby(temp_df.columns).mean().T  # Transpose, group by columns, then transpose back
        speed_data = pd.concat([speed_data, temp_df], ignore_index=True)

# Remove completely empty rows
speed_data.dropna(how='all', inplace=True)
# Perform linear interpolation to fill in missing values
data_interpolated = speed_data.interpolate(method='linear', axis=1)

print(data_interpolated.head())
print(data_interpolated.shape)

# Save the interpolated data to a CSV file
data_interpolated.to_csv('../hn_speed.csv', index=False)
