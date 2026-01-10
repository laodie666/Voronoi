import matplotlib.pyplot as plt

points  = [(0,0), (1,1), (-1,1)]
# Half plane can't be infinite in size so resort to very big
bigshape_constant = max(max([p[0] for p in points]), max([p[1] for p in points])) * 100

# Current Objective: Brute force drawing voronoi using half plane intersection, n^3 runtime
# Future Objective: Fortune's algorithm: https://en.wikipedia.org/wiki/Fortune%27s_algorithm

# Planning:
# For every point, draw the intersection of its halfplane with every other point, which result in it's cell.
# This is done by clipping polygons: https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm

def draw_line(line):
    p1 = line.p1
    p2 = line.p2
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]])

class line:
    p1 = (0,0)
    p2 = (0,0)
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def midpoint(self):
        return ((self.p1[0]+self.p2[0])/2, (self.p1[1]+self.p2[1])/2)
    
    def slope(self):
        return (self.p2[1]-self.p1[1])/(self.p2[0]-self.p1[0])
    
    def bisector(self):
        left_point = (self.midpoint()[0] - bigshape_constant, self.midpoint()[1] + 1/(self.slope()*bigshape_constant))
        right_point = (self.midpoint()[0] + bigshape_constant, self.midpoint()[1] - 1/(self.slope()*bigshape_constant))
        print(self.p1, self.p2)
        print(left_point, right_point)
        return line(left_point, right_point)

# Polygon is just a list of lines

l = line(points[0], points[1])
draw_line(l)
draw_line(l.bisector())

plt.xlim(-bigshape_constant/80, bigshape_constant/80)
plt.ylim(-bigshape_constant/80, bigshape_constant/80)

# plt.axis('off')
plt.show()



