import osmnx as ox
import geopandas as gpd

# Define the place of interest
place_name = "Hanoi, Vietnam"

# Get the boundary of Ba Dinh District
gdf = ox.geocode_to_gdf(place_name)

# Ensure the data is in GeoDataFrame format
if not isinstance(gdf, gpd.GeoDataFrame):
    gdf = gpd.GeoDataFrame(gdf)

# Save the boundary to a GeoJSON file
gdf.to_file("../Hanoi_boundary.geojson", driver="GeoJSON")

print("GeoJSON boundary saved to 'ba_dinh_boundary.geojson'")
