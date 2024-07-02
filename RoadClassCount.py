import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiLineString, LineString
from shapely.ops import unary_union

# Load the shapefile
shapefile_path = "./data/hanoi/network.shp"
gdf = gpd.read_file(shapefile_path)

# Ensure consistent CRS
gdf = gdf.to_crs(epsg=4326)

# Function to combine geometries by StreetName
def combine_geometries(gdf):
    combined_geometries = []
    street_names = []
    for name, group in gdf.groupby('StreetName'):
        combined_geom = unary_union(group.geometry)
        if isinstance(combined_geom, (LineString, MultiLineString)):
            combined_geometries.append(combined_geom)
            street_names.append(name)
    return gpd.GeoDataFrame({'StreetName': street_names, 'geometry': combined_geometries}, geometry='geometry')

# Function to filter by road class and visualize
def filter_and_visualize_by_frc(gdf, frc):
    filtered_gdf = gdf[gdf['FRC'] == frc]
    combined_gdf = combine_geometries(filtered_gdf)
    
    # Plot the combined GeoDataFrame
    fig, ax = plt.subplots(figsize=(15, 15))
    combined_gdf.plot(ax=ax, column='StreetName', legend=True, cmap='tab20')
    ax.set_title(f'Combined Road Segments by StreetName for Road Class {frc}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    # Plot the coordinates of each segment
    for geom in filtered_gdf.geometry:
        if geom.geom_type == 'LineString':
            x, y = geom.xy
            ax.plot(x, y, color='grey', linewidth=0.5, linestyle='--')
        elif geom.geom_type == 'MultiLineString':
            for part in geom:
                x, y = part.xy
                ax.plot(x, y, color='grey', linewidth=0.5, linestyle='--')
    
    plt.show()
    
    # Get the number of unique roads
    number_of_roads = combined_gdf.shape[0]
    print(f'Number of unique roads for road class {frc}: {number_of_roads}')

# Example usage
selected_frc = 3  # Change this to the desired road class
filter_and_visualize_by_frc(gdf, selected_frc)