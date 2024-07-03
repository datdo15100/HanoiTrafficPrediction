import geopandas as gpd
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import LineString, MultiLineString
from shapely.ops import unary_union

# Load the shapefile
shapefile_path = '../hanoi/network.shp'
gdf = gpd.read_file(shapefile_path)

# Filter based on multiple FRCs
selected_frcs = [3, 4]  # Change this to the desired FRCs
gdf = gdf[gdf['FRC'].isin(selected_frcs)]

# Combine segments by StreetName
combined_gdf = gdf.dissolve(by='StreetName')

# Create a graph using NetworkX
G = nx.Graph()

# Add each combined road segment as a node
for idx, row in combined_gdf.iterrows():
    geom = row.geometry
    if isinstance(geom, LineString) or isinstance(geom, MultiLineString):
        G.add_node(idx, geometry=geom, name=idx)

# Add edges between nodes if their road segments intersect
for i, geom1 in combined_gdf.geometry.items():
    for j, geom2 in combined_gdf.geometry.items():
        if i != j and geom1.intersects(geom2):
            G.add_edge(i, j)

# Extract positions for plotting (using centroid of each road segment)
pos = {idx: (geom.centroid.x, geom.centroid.y) for idx, geom in combined_gdf.geometry.items()}

# Plot the graph
plt.figure(figsize=(15, 15))
nx.draw(G, pos, with_labels=True, labels={idx: idx for idx in G.nodes}, node_size=15, node_color='blue', edge_color='gray')
plt.title(f"Road Network with Road Classes {selected_frcs}")
plt.show()

# Convert adjacency matrix to a DataFrame for better visualization
adj_matrix = nx.adjacency_matrix(G).todense()
adj_df = pd.DataFrame(adj_matrix, index=combined_gdf.index, columns=combined_gdf.index)

# Save adjacency matrix to a CSV file
adj_df.to_csv('../hn_adj.csv', header=False, index=False)
