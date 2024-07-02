import os
import geopandas as gpd
import pickle

def read_speed_data(root_folder):
    speed_data_dict = {}
    
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.dbf'):
                file_path = os.path.join(subdir, file)
                gdf = gpd.read_file(file_path)
                
                # Extract a unique identifier for the DataFrame (e.g., folder and filename)
                identifier = os.path.relpath(file_path, root_folder)
                speed_data_dict[identifier] = gdf
    
    return speed_data_dict

# Example usage
root_folder = '../hanoi/'  # Replace with the path to your root folder containing speed data
speed_data_dict = read_speed_data(root_folder)

# Save the dictionary of DataFrames to a pickle file
SAVE_FILE = "../hanoi/all_dataframes_final.pkl"

with open(SAVE_FILE, 'wb') as f:
    pickle.dump(speed_data_dict, f)

print(f"Saved all speed data to {SAVE_FILE}")

# Example: Accessing a specific DataFrame from the saved pickle file
with open(SAVE_FILE, 'rb') as f:
    loaded_speed_data_dict = pickle.load(f)

example_key = list(loaded_speed_data_dict.keys())[0]
example_df = loaded_speed_data_dict[example_key]
print(f"Loaded DataFrame for {example_key} with shape {example_df.shape}")
print(example_df.head())
