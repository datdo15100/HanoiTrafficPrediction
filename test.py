import geopandas as gpd

# Path to the shapefile
file_path = './data/hanoi/network.shp'

# Read the shapefile
shapefile_data = gpd.read_file(file_path)

# Display the first few rows of the data
shapefile_data.head()
