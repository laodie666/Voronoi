# A brute force way of drawing Voronoi diagrams

<img width="638" height="549" alt="image" src="https://github.com/user-attachments/assets/c725d54a-7887-4e4d-bbc6-a4f5b81e547f" />


The implementation is of O(n^3) runtime, utilizing the fact that a cell for a datapoint in the Voronoi diagram is the intersection of all the closed half-spaces bounded by the perpendicular bisector it has with every other point.


The intersection is implemented using the Sutherland–Hodgman algorithm to clip polygons by the perpendicular bisectors to form the cell for each point.


Referencing: https://en.wikipedia.org/wiki/Voronoi_diagram
https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm
