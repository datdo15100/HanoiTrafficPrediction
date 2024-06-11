import requests
import zipfile
import os
from io import BytesIO
import pandas as pd
from dbfread import DBF
import re
import pickle
from dotenv import load_dotenv

load_dotenv()

# Function to download and extract shapefiles for a given ID
def download_and_extract_shapefiles(base_url, api_key, job_id, output_base_dir):
    # API request URL
    api_url = f"{base_url}/{job_id}?key={api_key}"
    
    # Make the API request to get the job details
    # response = requests.get(api_url)
    # job_details = response.json()
    
    # Extract the URL for the shapefile zip from the API response
    # shapefile_url = job_details['urls'][2]
    
    # Create a directory for this job ID
    output_dir = os.path.join(output_base_dir, str(job_id))
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the zip file
    # response = requests.get(shapefile_url)
    # zip_file = zipfile.ZipFile(BytesIO(response.content))
    
    # Extract all files from the zip archive
    # zip_file.extractall(output_dir)
    
    # Regular expression to match files with dates in their names
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    
    # Read all DBF files with dates in the extracted directory
    dbf_files = [file for file in os.listdir(output_dir) if file.endswith('.dbf') and date_pattern.search(file)]
    
    # Store the dataframes
    dataframes = {}

    for dbf_file in dbf_files:
        dbf_path = os.path.join(output_dir, dbf_file)
        # Read the DBF file
        table = DBF(dbf_path)
        df = pd.DataFrame(iter(table))
        # Store the DataFrame in a dictionary with the filename as the key
        dataframes[dbf_file] = df

    return dataframes

# Constants
BASE_URL = "https://api.tomtom.com/traffic/trafficstats/status/1"
API_KEY = os.getenv('TOMTOM_KEY')
START_ID = 4383493
NUM_DAYS = 19
OUTPUT_BASE_DIR = "../hanoi"
SAVE_FILE = "../hanoi/all_dataframes.pkl"

# Dictionary to store all DataFrames from all days
all_dataframes = {}

# Loop through the 20 IDs
for day in range(NUM_DAYS):
    job_id = START_ID + day
    day_dataframes = download_and_extract_shapefiles(BASE_URL, API_KEY, job_id, OUTPUT_BASE_DIR)
    all_dataframes[job_id] = day_dataframes

# Save the dictionary of all DataFrames to a file
with open(SAVE_FILE, 'wb') as f:
    pickle.dump(all_dataframes, f)

# Example: how to read the saved data back
with open(SAVE_FILE, 'rb') as f:
    loaded_dataframes = pickle.load(f)

# Print the loaded data to verify
for job_id, day_dataframes in loaded_dataframes.items():
    print(f"Data from job {job_id}:")
    for filename, dataframe in day_dataframes.items():
        print(f"Data from {filename}:")
        print(dataframe.head())  # Display the first few rows of each dataframe
        print("\n")
