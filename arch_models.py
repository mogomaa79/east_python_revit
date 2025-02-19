from math import sqrt
from shapely.geometry import Polygon
from shapely import Point

class Rectangle:
    def __init__(self, limits_x, limits_y):
        self.polygon = Polygon([(limits_x[0], limits_y[0]), (limits_x[1], limits_y[0]), (limits_x[1], limits_y[1]), (limits_x[0], limits_y[1])])
        self.limits_x = limits_x
        self.limits_y = limits_y

    def intersects(self, x, y):
        return self.polygon.intersects(Point(x, y))

    def limited(self, x, y, dx, dy, canti_dist):
        if dx == 0:
            return abs(y - self.limits_y[0]) < canti_dist or abs(y - self.limits_y[1]) < canti_dist
        elif dy == 0:
            return abs(x - self.limits_x[0]) < canti_dist or abs(x - self.limits_x[1]) < canti_dist
        return False

class L_shape(Rectangle):
    def __init__(self, rectangle1, rectangle2):
        self.rectangle1 = rectangle1
        self.rectangle2 = rectangle2
    
    def intersects(self, x, y):
        return self.rectangle1.intersects(x, y) or self.rectangle2.intersects(x, y)
    
    def limited(self, x, y, dx, dy, canti_dist):
        return self.rectangle1.limited(x, y, dx, dy, canti_dist) or self.rectangle2.limited(x, y, dx, dy, canti_dist)
    
class T_shape(L_shape):
    pass

class Circle:
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
    
    def intersects(self, x, y):
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= self.r ** 2
    
    def limited(self, x, y, dx, dy, canti_dist):
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= (self.r + canti_dist) ** 2

class Torus:
    def __init__(self, r1, r2):
        center = r1 * sqrt(2), r1 * sqrt(2)
        self.circle1 = Circle(center[0], center[1], r1)
        self.circle2 = Circle(center[0], center[1], r2)
    
    def intersects(self, x, y):
        return self.circle1.intersects(x, y) and not self.circle2.intersects(x, y)
    
    def limited(self, x, y, dx, dy, canti_dist):
        return self.circle1.limited(x, y, dx, dy, canti_dist) or self.circle2.limited(x, y, dx, dy, canti_dist)
    
class Triangle:
    def __init__(self, p1, p2, p3):
        self.polygon = Polygon([p1, p2, p3])
    
    def intersects(self, x, y):
        return self.polygon.intersects(Point(x, y))
    
    def limited(self, x, y, dx, dy, canti_dist):
        """Check if point is near the edge of the triangle by canti_dist"""
        return self.polygon.boundary.distance(Point(x, y)) < canti_dist

class Villa:
    def __init__(self, rectangle1, rectangle2, rectangle3, rectangle4, triangle):
        self.rectangle1 = rectangle1
        self.rectangle2 = rectangle2
        self.rectangle3 = rectangle3
        self.rectangle4 = rectangle4
        self.triangle = triangle

    def intersects(self, x, y):
        return self.rectangle1.intersects(x, y) or self.rectangle2.intersects(x, y) or self.rectangle3.intersects(x, y) or self.rectangle4.intersects(x, y) or self.triangle.intersects(x, y)
    
    def limited(self, x, y, dx, dy, canti_dist):
        return self.rectangle1.limited(x, y, dx, dy, canti_dist) or self.rectangle2.limited(x, y, dx, dy, canti_dist) or self.rectangle3.limited(x, y, dx, dy, canti_dist) or self.rectangle4.limited(x, y, dx, dy, canti_dist) or self.triangle.limited(x, y, dx, dy, canti_dist)
        

class Obstacle(Rectangle):
    def __init__(self, x, y):
        """x -- x of lowermost left point, y -- y of lowermost left point"""
        super().__init__((x, x + 0.3), (y, y + 0.45))
