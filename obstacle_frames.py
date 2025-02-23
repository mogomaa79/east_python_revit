from obstacle_trad import *

class Frames(TraditionalProps):
    def __init__(self, frame_dist, min_dist, vertical_dist, obstacles, shape, canti_dist=0):
        super().__init__(min_dist, obstacles, shape, canti_dist)
        self.frame_dist = frame_dist
        self.scale = 1
        self.min_dist = min_dist
        self.vertical_dist = vertical_dist
        self.canti_dist = canti_dist
        self.props = set()
        self.cantilevers = set()

    def is_valid_position(self, x, y):
        return self.shape.intersects(x, y) and not self.is_inside_obstacle(x, y) and not self.is_near_another_prop(x, y)
    
    def generate_props(self):
        """Fill the props list with the props generated. 
        Distance in horizontal and vertical are defined by the user.
        Frames dist is the distance between two props in the frame"""
        x, y = (self.start_point)
        while not self.is_valid_position(x, y) or not self.is_valid_position(x + self.frame_dist, y):
            x += 0.1
        x, y = round(x, 2), round(y, 2)
        self.props = {(x, y), (x + self.frame_dist, y)}
        directions = [(self.min_dist, 0), (-self.min_dist, 0), (0, self.min_dist), (0, -self.min_dist)]
        queue = [(x, y), (x + self.frame_dist, y)]
        visited = set(queue)

        while queue:
            current_x, current_y = queue.pop(0)
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if (new_x, new_y) not in visited and self.is_valid_position(new_x, new_y) and self.is_valid_position(new_x + self.frame_dist, new_y):
                    new_x, new_y = round(new_x, 2), round(new_y, 2)
                    self.props.add((new_x, new_y))
                    self.props.add((new_x + self.frame_dist, new_y))
                    queue.append((new_x, new_y))
                    queue.append((new_x + self.frame_dist, new_y))
                    visited.add((new_x, new_y))
                    visited.add((new_x + self.frame_dist, new_y))

    def is_near_another_prop(self, x, y):
        for prop in self.props - {(x, y)}:
            if abs(prop[0] - x) < self.min_dist and abs(prop[1] - y) < self.min_dist:
                return True
        return False
    
    def generate_cantilevers(self):
        """If there is a gap after the last frame in any direction.
        Fill the gap with a prop in the midpoint till the edge."""
        # get the max x and y values from the props
        max_x = max(self.props, key=lambda x: x[0])[0]
        max_y = max(self.props, key=lambda x: x[1])[1]

        min_x = min(self.props, key=lambda x: x[0])[0]
        min_y = min(self.props, key=lambda x: x[1])[1]

        # loop over all props at the max or min values
        for x, y in self.props.copy():
            if x == max_x and (dist := self.shape.nearest_bdist(max_x, y)):
                if dist >= self.canti_dist:
                    self.cantilevers.add((max_x + self.canti_dist, y))
                if dist > self.canti_dist:
                    self.props.add((max_x + dist, y))
            if x == min_x and (dist := self.shape.nearest_bdist(min_x, y)):
                if dist >= self.canti_dist:
                    self.cantilevers.add((min_x - self.canti_dist, y))
                if dist > self.canti_dist:
                    self.props.add((min_x + dist, y))
            
            if y == max_y and (dist := self.shape.nearest_bdist(x, max_y)):
                if dist >= self.canti_dist:
                    self.cantilevers.add((x, max_y + self.canti_dist))
                if dist > self.canti_dist:
                    self.props.add((x, max_y + dist))
            
            if y == min_y and (dist := self.shape.nearest_bdist(x, min_y)):
                if dist >= self.canti_dist:
                    self.cantilevers.add((x, min_y - self.canti_dist))
                if dist > self.canti_dist:
                    self.props.add((x, min_y + dist))

def main():
    frame_dist = 1.2
    min_dist = 1
    vertical_dist = 1
    obstacles = [Obstacle(0, 0), Obstacle(2, 2), Obstacle(7, 7)]
    villa = Villa(
        Rectangle([0, 4.75], [0, 16.3]),
        Rectangle([4.75, 9.8], [1.91, 16.3]),
        Rectangle([9.8, 15.45], [2.76, 16.3]),
        Rectangle([15.45, 23.4], [10.8, 16.3]),
        Triangle([15.45, 2.76], [15.4, 10.8], [23.4, 10.8])
    )
    canti_dist = 0.4
    frames = Frames(frame_dist, min_dist, vertical_dist, obstacles, villa, canti_dist)
    frames.generate_props()
    frames.generate_cantilevers()
    frames.plot()

if __name__ == '__main__':
    main()
