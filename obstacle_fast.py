from obstacle_frames import *

class Fast(Frames):
    def __init__(self, frame_dist, horizontal_dist, vertical_dist, obstacles, shape):
        super().__init__(horizontal_dist, obstacles, shape)
        self.frame_dist = frame_dist
        self.horizontal_dist = horizontal_dist
        self.vertical_dist = vertical_dist

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
        self.props = [(x, y), (x + self.frame_dist, y)]
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
                    self.props.append((new_x, new_y))
                    self.props.append((new_x + self.frame_dist, new_y))
                    queue.append((new_x, new_y))
                    queue.append((new_x + self.frame_dist, new_y))
                    visited.add((new_x, new_y))
                    visited.add((new_x + self.frame_dist, new_y))
                    self.frames.append((new_x, new_y, new_x + self.frame_dist, new_y))

    def is_inside_obstacle(self, x, y):
        for obs in self.obstacles:
            if (obs[0] < x < obs[2] and obs[1] < y < obs[3]) \
                or (obs[0] < x + self.frame_dist < obs[2] and obs[1] < y < obs[3]) \
                    or (x < obs[0] and x + self.frame_dist > obs[2] and obs[1] < y < obs[3]):
                return True
        return False

    def is_valid_position(self, x, y):
        if (
            x < self.limits_x[0] or x > self.limits_x[1] or
            y < self.limits_y[0] or y > self.limits_y[1] or
            self.is_between_frame(x, y)
        ):
            return False
        return not self.is_near_another_prop(x, y)


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
    

def main():
    frame_dist = 2.5
    horizontal_dist = 0.15
    vertical_dist = 1.8
    obstacles = [Obstacle(0, 0), Obstacle(2, 2), Obstacle(7, 7)]
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
