import geopandas as gpd
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import osmnx as ox

# Load the shapefile
shapefile_path = '../hanoi/network.shp'
gdf = gpd.read_file(shapefile_path)

# Fetch the boundary of Ba Dinh district from OpenStreetMap
# ba_dinh_boundary = ox.geocode_to_gdf('Hanoi, Vietnam')

# Ensure the CRS matches between the shapefile and the boundary
# gdf = gdf.to_crs(ba_dinh_boundary.crs)

# Clip the road network to the boundary of Ba Dinh district
# gdf_clipped = gpd.clip(gdf, ba_dinh_boundary)

gdf_clipped = gdf

# # Combine Segments into Streets
# gdf_clipped = gdf_clipped.dissolve(by='StreetName')

# Create a graph using NetworkX
G = nx.Graph()

# Add each combined road segment as a node
for idx, geom in enumerate(gdf_clipped.geometry):
    if isinstance(geom, LineString):
        G.add_node(idx, geometry=geom, name=gdf_clipped.index[idx])

# Add edges between nodes if their road segments intersect
for i, geom1 in enumerate(gdf_clipped.geometry):
    for j, geom2 in enumerate(gdf_clipped.geometry):
        if i != j and geom1.intersects(geom2):
            G.add_edge(i, j)

# Extract positions for plotting (using centroid of each road segment)
pos = {idx: (geom.centroid.x, geom.centroid.y) for idx, geom in enumerate(gdf_clipped.geometry)}

# Plot the graph
plt.figure(figsize=(15, 15))
nx.draw(G, pos, with_labels=True, labels={idx: gdf_clipped.index[idx] for idx in G.nodes}, node_size=15, node_color='blue', edge_color='gray')
plt.title("Road Network of Ba Dinh District, Hanoi")
plt.show()

# Convert adjacency matrix to a DataFrame for better visualization
adj_matrix = nx.adjacency_matrix(G).todense()
adj_df = pd.DataFrame(adj_matrix, index=gdf_clipped.index, columns=gdf_clipped.index)

# Save adjacency matrix to a CSV file
adj_df.to_csv('../hn_adj.csv', header=False, index=False)
