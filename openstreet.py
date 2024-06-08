import geopandas as gpd
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import osmnx as ox

# Load the shapefile
shapefile_path = './data/hanoi/network.shp'
gdf = gpd.read_file(shapefile_path)

# Fetch the boundary of Ba Dinh district from OpenStreetMap
ba_dinh_boundary = ox.geocode_to_gdf('Ba Dinh, Hanoi, Vietnam')

# Ensure the CRS matches between the shapefile and the boundary
gdf = gdf.to_crs(ba_dinh_boundary.crs)

# Clip the road network to the boundary of Ba Dinh district
gdf_clipped = gpd.clip(gdf, ba_dinh_boundary)

# Display the first few rows and columns to identify a suitable attribute
print(gdf_clipped.head())
print(gdf_clipped.columns)

# Assuming 'your_attribute' is the column that identifies the road name
# Replace 'your_attribute' with the actual column name

# gdf_combined = gdf_clipped.dissolve(by='StreetName')
gdf_combined = gdf_clipped

# Create a graph using NetworkX
G = nx.Graph()

# Add each combined road segment as a node
for idx, geom in enumerate(gdf_combined.geometry):
    if isinstance(geom, LineString):
        G.add_node(idx, geometry=geom, name=gdf_combined.index[idx])

# Add edges between nodes if their road segments intersect
for i, geom1 in enumerate(gdf_combined.geometry):
    for j, geom2 in enumerate(gdf_combined.geometry):
        if i != j and geom1.intersects(geom2):
            G.add_edge(i, j)

# Extract positions for plotting (using centroid of each road segment)
pos = {idx: (geom.centroid.x, geom.centroid.y) for idx, geom in enumerate(gdf_combined.geometry)}

# Plot the graph
plt.figure(figsize=(10, 10))
nx.draw(G, pos, with_labels=True, labels={idx: gdf_combined.index[idx] for idx in G.nodes}, node_size=50, node_color='blue', edge_color='gray')
plt.title("Road Network of Ba Dinh District, Hanoi")
plt.show()

# Convert adjacency matrix to a DataFrame for better visualization
adj_matrix = nx.adjacency_matrix(G).todense()
adj_df = pd.DataFrame(adj_matrix, index=gdf_combined.index, columns=gdf_combined.index)

# Save adjacency matrix to a CSV file
adj_df.to_csv('./data/adjacency_matrix_ba_dinh.csv')

# Display the adjacency matrix
print(adj_df)
