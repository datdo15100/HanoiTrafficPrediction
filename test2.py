import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

# Define the geometries
line = LineString([(0, 0), (1, 1)])
point1 = Point(0, 0)
point2 = Point(0, 1)
line2 = LineString([(0, 2), (2, 0)])

# Check intersections
intersects_point1 = line.intersects(point1)
intersects_point2 = line.intersects(point2)
intersects_line2 = line.intersects(line2)

# Create the plot
fig, ax = plt.subplots()

# Plot the main line
x, y = line.xy
ax.plot(x, y, label="Line (0,0) to (1,1)")

# Plot the points
ax.plot(*point1.xy, 'go' if intersects_point1 else 'ro', label="Point (0,0) intersects")
ax.plot(*point2.xy, 'go' if intersects_point2 else 'ro', label="Point (0,1) does not intersect")

# Plot the second line
x2, y2 = line2.xy
ax.plot(x2, y2, label="Line (0,2) to (2,0) intersects" if intersects_line2 else "Line (0,2) to (2,0) does not intersect")

# Setting the legend
ax.legend()

# Display the plot
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Geometrical Intersections')
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.show()
