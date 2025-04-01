from math import sqrt
from shapely.geometry import Polygon
from shapely import Point, LineString


class Rectangle:
    def __init__(self, limits_x, limits_y):
        self.polygon = Polygon(
            [
                (limits_x[0], limits_y[0]),
                (limits_x[1], limits_y[0]),
                (limits_x[1], limits_y[1]),
                (limits_x[0], limits_y[1]),
            ]
        )
        self.limits_x = limits_x
        self.limits_y = limits_y

    def intersects(self, x, y):
        return self.polygon.intersects(Point(x, y))

    def limited(self, x, y, dx, dy, canti_dist):
        if dx == 0:
            return (
                abs(y - self.limits_y[0]) < canti_dist
                or abs(y - self.limits_y[1]) < canti_dist
            )
        elif dy == 0:
            return (
                abs(x - self.limits_x[0]) < canti_dist
                or abs(x - self.limits_x[1]) < canti_dist
            )
        return False

    def nearest_bdist(self, x, y):
        """Get the distance to the nearest boundary."""
        boundary = self.polygon.boundary
        nearest_point = boundary.interpolate(boundary.project(Point(x, y)))
        dist_x, dist_y = nearest_point.x - x, nearest_point.y - y
        if abs(dist_x) < abs(dist_y):
            return dist_x
        return dist_y


class L_shape(Rectangle):
    def __init__(self, rectangle1, rectangle2):
        self.rectangle1 = rectangle1
        self.rectangle2 = rectangle2

    def intersects(self, x, y):
        return self.rectangle1.intersects(x, y) or self.rectangle2.intersects(x, y)

    def limited(self, x, y, dx, dy, canti_dist):
        return self.rectangle1.limited(
            x, y, dx, dy, canti_dist
        ) or self.rectangle2.limited(x, y, dx, dy, canti_dist)

    def nearest_bdist(self, x, y):
        d1, d2 = self.rectangle1.nearest_bdist(x, y), self.rectangle2.nearest_bdist(
            x, y
        )
        if abs(d1) < abs(d2):
            return d1
        return d2


class T_shape(L_shape):
    pass


class Circle:
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r

    def intersects(self, x, y):
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= self.r**2

    def limited(self, x, y, dx, dy, canti_dist):
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= (self.r + canti_dist) ** 2

    def nearest_bdist(self, x, y):
        return abs(sqrt((x - self.cx) ** 2 + (y - self.cy) ** 2) - self.r)


class Torus:
    def __init__(self, r1, r2):
        center = r1, r1
        self.circle1 = Circle(center[0], center[1], r1)
        self.circle2 = Circle(center[0], center[1], r2)

    def intersects(self, x, y):
        return self.circle1.intersects(x, y) and not self.circle2.intersects(x, y)

    def limited(self, x, y, dx, dy, canti_dist):
        return self.circle1.limited(x, y, dx, dy, canti_dist) or self.circle2.limited(
            x, y, dx, dy, canti_dist
        )

    def nearest_bdist(self, x, y):
        return min(self.circle1.nearest_bdist(x, y), self.circle2.nearest_bdist(x, y))


class Triangle:
    def __init__(self, p1, p2, p3):
        self.polygon = Polygon([p1, p2, p3])

    def intersects(self, x, y):
        return self.polygon.intersects(Point(x, y))

    def limited(self, x, y, dx, dy, canti_dist):
        """Check if point is near the edge of the triangle by canti_dist"""
        return self.polygon.boundary.distance(Point(x, y)) < canti_dist

    def nearest_bdist(self, x, y):
        return self.polygon.boundary.distance(Point(x, y))


class Villa:
    def __init__(self, rectangle1, rectangle2, rectangle3, rectangle4, triangle):
        self.rectangle1 = rectangle1
        self.rectangle2 = rectangle2
        self.rectangle3 = rectangle3
        self.rectangle4 = rectangle4
        self.triangle = triangle

    def intersects(self, x, y):
        return (
            self.rectangle1.intersects(x, y)
            or self.rectangle2.intersects(x, y)
            or self.rectangle3.intersects(x, y)
            or self.rectangle4.intersects(x, y)
            or self.triangle.intersects(x, y)
        )

    def limited(self, x, y, dx, dy, canti_dist):
        return (
            self.rectangle1.limited(x, y, dx, dy, canti_dist)
            or self.rectangle2.limited(x, y, dx, dy, canti_dist)
            or self.rectangle3.limited(x, y, dx, dy, canti_dist)
            or self.rectangle4.limited(x, y, dx, dy, canti_dist)
            or self.triangle.limited(x, y, dx, dy, canti_dist)
        )

    def nearest_bdist(self, x, y):
        return min(
            self.rectangle1.nearest_bdist(x, y),
            self.rectangle2.nearest_bdist(x, y),
            self.rectangle3.nearest_bdist(x, y),
            self.rectangle4.nearest_bdist(x, y),
            self.triangle.nearest_bdist(x, y),
        )


class Obstacle(Rectangle):
    def __init__(self, x, y):
        """x -- x of lowermost left point, y -- y of lowermost left point"""
        super().__init__((x, x + 0.3), (y, y + 0.45))

    def intersects_frame(self, x1, x2, y):
        """Check if the horizontal line segment from (x1, y) to (x2, y) intersects the rectangle."""
        return (
            self.polygon.intersects(Point(x1, y))
            or self.polygon.intersects(Point(x2, y))
            or x1 < self.limits_x[0]
            and x2 > self.limits_x[1]
            and y > self.limits_y[0]
            and y < self.limits_y[1]
        )
