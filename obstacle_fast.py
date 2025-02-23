from obstacle_frames import *
from shapely import LineString

class Fast(Frames):
    def __init__(self, frame_dist, horizontal_dist, vertical_dist, obstacles, shape):
        super().__init__(frame_dist, horizontal_dist, vertical_dist, obstacles, shape)
        self.horizontal_dist = horizontal_dist
        self.frames = []

    def is_valid_position(self, x, y):
        return self.shape.intersects(x, y) and not self.is_inside_obstacle(x, y) and not self.is_near_another_prop(x, y)

    def generate_props(self):
        """Fill the props list with the props generated. 
        Distance in horizontal and vertical are defined by the user.
        Frame dist is the distance between two props in the frame."""
        x, y = self.start_point
        while not self.is_valid_position(x, y) or not self.is_valid_position(x + self.frame_dist, y):
            x += 0.05
        x, y = round(x, 3), round(y, 3)
        self.props = {(x, y), (x + self.frame_dist, y)}
        self.frames.append((x, y, x + self.frame_dist, y))
        directions = [(self.horizontal_dist, 0), (-self.horizontal_dist, 0), (0, self.vertical_dist), (0, -self.vertical_dist)]
        queue = [(x, y), (x + self.frame_dist, y)]
        visited = set(queue)

        while queue:
            current_x, current_y = queue.pop(0)
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if (
                    (new_x, new_y) not in visited 
                    and self.is_valid_position(new_x, new_y) 
                    and self.is_valid_position(new_x + self.frame_dist, new_y)
                    and not self.is_inside_obstacle(new_x, new_y)
                ):
                    new_x, new_y = round(new_x, 3), round(new_y, 3)
                    self.props.add((new_x, new_y))
                    self.props.add((new_x + self.frame_dist, new_y))
                    queue.append((new_x, new_y))
                    queue.append((new_x + self.frame_dist, new_y))
                    visited.add((new_x, new_y))
                    visited.add((new_x + self.frame_dist, new_y))
                    self.frames.append((new_x, new_y, new_x + self.frame_dist, new_y))

    def is_inside_obstacle(self, x, y):
        return any(obs.intersects(LineString([[x, y], [x + self.frame_dist, y]])) for obs in self.obstacles)

    def is_valid_position(self, x, y):
        return self.shape.intersects(x, y) and \
              not self.is_inside_obstacle(x, y) and \
                  not self.is_near_another_prop(x, y) and \
                        not self.is_between_frame(x, y)

    def is_between_frame(self, x, y):
        for frame in self.frames:
            if frame[0] < x < frame[2] and frame[1] == y:
                return True
        return False
    
    def is_near_another_prop(self, x, y, epsilon=1e-2):
        """Check if (x, y) is near an existing prop within defined horizontal and vertical distances."""
        for prop in self.props:
            if abs(prop[0] - x) + epsilon < self.horizontal_dist and abs(prop[1] - y) + epsilon < self.vertical_dist:
                return True      
        return False
    
    def place_final_prop(self):
        """If there is a gap after the last frame in any direction.
        Fill the gap with a prop in the midpoint till the edge."""
        # get the max x and y values from the props
        max_x = max(self.props, key=lambda x: x[0])[0]
        max_y = max(self.props, key=lambda x: x[1])[1]

        min_x = min(self.props, key=lambda x: x[0])[0]
        min_y = min(self.props, key=lambda x: x[1])[1]

        # loop over all props at the max or min values
        for x, y in self.props.copy():
            if x == max_x:
                dist = self.shape.nearest_bdist(max_x, y)
                self.props.add((max_x + dist // 2, y))

            if x == min_x:
                dist = self.shape.nearest_bdist(min_x, y)
                self.props.add((min_x + dist // 2, y))
            
            if y == max_y:
                dist = self.shape.nearest_bdist(x, max_y)
                self.props.add((x, max_y + dist // 2))
            
            if y == min_y:
                dist = self.shape.nearest_bdist(x, min_y)
                self.props.add((x, min_y + dist // 2))
    

def main():
    frame_dist = 2.5
    horizontal_dist = 0.15
    vertical_dist = 1.8
    obstacles = [Obstacle(0, 0), Obstacle(2, 2)]
    villa = Villa(
        Rectangle([0, 4.75], [0, 16.3]),
        Rectangle([4.75, 9.8], [1.91, 16.3]),
        Rectangle([9.8, 15.45], [2.76, 16.3]),
        Rectangle([15.45, 23.4], [10.8, 16.3]),
        Triangle([15.45, 2.76], [15.4, 10.8], [23.4, 10.8])
    )
    fast = Fast(frame_dist, horizontal_dist, vertical_dist, obstacles, villa)
    fast.generate_props()
    fast.place_final_prop()
    fast.plot()

if __name__ == '__main__':
    main()
