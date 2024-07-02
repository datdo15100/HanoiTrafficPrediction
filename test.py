import geopandas as gpd

# Correct path to the network shapefile
shapefile_path = r'C:\Users\ADMIN\Desktop\T-GCN-PyTorch\data\hanoi\network.shp'

# Load the shapefile
gdf_network = gpd.read_file(shapefile_path)

# Print attributes and their values for the first few records
for idx, row in gdf_network.iterrows():
    print(f"Record {idx}:")
    for col in gdf_network.columns:
        print(f"  {col}: {row[col]}")
    print("\n")
    if idx >= 4:  # Print only the first 5 records for brevity
        break
