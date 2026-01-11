import matplotlib.pyplot as plt

points  = [(0,0), (2,0), (2,2)]
# Half plane can't be infinite in size so resort to very big
bigshape_constant = max(max([p[0] for p in points]), max([p[1] for p in points]), 10) * 100

# Comment: Really should be working with homogeneous coordinates in future projects like this, to represent lines points and intersections much easier. 

# Current Objective: Brute force drawing voronoi using half plane intersection, n^3 runtime
# Future Objective: Fortune's algorithm: https://en.wikipedia.org/wiki/Fortune%27s_algorithm

# Planning:
# For every point, draw the intersection of its halfplane with every other point, which result in it's cell.
# This is done by clipping polygons: https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm

def draw_line(line):
    p1 = line.p1
    p2 = line.p2
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='black')

def draw_point(p):
    plt.plot([p[0]],[p[1]], 'ro')

def add_points(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1])

def subtract_points(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1])

def dot_product(v1, v2):
    output = 0
    for i in range(len(v1)):
        output += v1[i] * v2[i]
    return output

def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

# Whether p is left, on, or right of l using cross product. 
# >0 is left, =0 is on, <0 is right
def left_of_line(l, p):
    return (l.p2[0] - l.p1[0])*(p[1] - l.p1[1]) - (l.p2[1] - l.p1[1])*(p[0] - l.p1[0]) > 0

class line:
    p1 = (0,0)
    p2 = (0,0)
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    # y = a + mx
    def a(self):
        return (self.p1[1] - self.p1[0]*self.slope())

    def midpoint(self):
        return ((self.p1[0]+self.p2[0])/2, (self.p1[1]+self.p2[1])/2)
    
    def slope(self):
        if self.p1[0] == self.p2[0]:
            return float("inf")
        return (self.p2[1]-self.p1[1])/(self.p2[0]-self.p1[0])
    
    def bisector(self):
        if self.slope() == 0:
            return (line((self.midpoint()[0], -bigshape_constant), (self.midpoint()[0], bigshape_constant)))

        perp = -1/self.slope()

        left_point = (self.midpoint()[0] - bigshape_constant, self.midpoint()[1] - bigshape_constant * perp)
        right_point = (self.midpoint()[0] + bigshape_constant, self.midpoint()[1] + bigshape_constant * perp)
        return line(left_point, right_point)

    # Return intersect point with another line, return None if DNE.
    def intersect(self, other: "line"):
        # don't intersect
        if self.slope() == other.slope() and self.a() == other.a():
            return None
        # same line
        if self.slope() == other.slope() and self.a() != other.a():
            return None

        # Degenerate case, really should use homogeneous coordinates
        if other.slope() == float("inf"):
            x = other.p1[0]
            y = self.a() + self.slope() * x
        elif self.slope() == float("inf"):
            x = self.p1[0]
            y = other.a() + other.slope() * x
        else:  
            x = (other.a() - self.a())/(self.slope() - other.slope()) 
            y = self.a() + self.slope() * x

        if min(self.p1[0], self.p2[0]) <= x <= max(self.p1[0], self.p2[0]) and \
            min(other.p1[0], other.p2[0]) <= x <= max(other.p1[0], other.p2[0]):
            return (x,y)    
        else:
            return None
    


class polygon:
    def __init__(self):
        self.lines = []


def draw_voronoi_for_p(point):
# Say line a is being clipped by line b, representing point at 1 -1
    output = polygon()
    i = 0
    for other in points:
        
        if other == point:
            continue

        if len(output.lines) == 0:
            l = line(point, other)
            output.lines.append(l.bisector())
            continue

        result = polygon()
        for la in output.lines:
            
            lb = line(point, other)
            lb = lb.bisector()

            start = la.p1
            intersect = la.intersect(lb)
            if intersect != None:
                # Check whether the source of the line is the same side as the point against the bisector
                # They are of opposite sides, meaning the line is entering
                if left_of_line(lb, la.p1) != left_of_line(lb, point):
                    result.lines.append(line(intersect, la.p2))
                # Line is exiting
                else:
                    result.lines.append(line(start, intersect))
                    # Determine which end of lb to add
                    if left_of_line(la, point) == left_of_line(lb, point):
                        result.lines.append(line(intersect, lb.p2))     
                    else:
                        result.lines.append(line(intersect, lb.p1))

            # If no intersection
            else:
                # If inside just add the line segment
                if dot_product(subtract_points(la.p1, lb.p1), subtract_points(point, lb.p1)) > 0:
                    result.lines.append(la)
                # If outside discard

        output = result
    
    for l in output.lines:
        draw_line(l)
                        

for point in points:
    draw_voronoi_for_p(point)

    draw_point(point)
    

xs = [p[0] for p in points]
ys = [p[1] for p in points]

cx = (min(xs) + max(xs)) / 2
cy = (min(ys) + max(ys)) / 2

span = max(max(xs) - min(xs), max(ys) - min(ys), 1)

plt.xlim(cx - span, cx + span)
plt.ylim(cy - span, cy + span)

# plt.axis('off')
plt.show()



