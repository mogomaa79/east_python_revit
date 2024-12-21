import matplotlib.pyplot as plt

class Fast:
    def __init__(self, start_point, frame_dist, horizontal_dist, vertical_dist, obstacles, limits_x, limits_y, canti_dist):
        self.start_point = start_point
        self.frame_dist = frame_dist
        self.obstacles = obstacles
        self.limits_x = limits_x
        self.limits_y = limits_y
        self.canti_dist = canti_dist
        self.horizontal_dist = horizontal_dist
        self.vertical_dist = vertical_dist
        self.frames = []
        self.props = []
        self.cantilevers = []

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
                self.props.append((max_x + (self.limits_x[1] - max_x) // 2, y))
            if x == min_x:
                self.props.append((min_x - (min_x - self.limits_x[0]) // 2, y))
            if y == max_y:
                self.props.append((x, max_y + (self.limits_y[1] - max_y) // 2))
            if y == min_y:
                self.props.append((x, min_y - (min_y - self.limits_y[0]) // 2))


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
    
    def generate_cantilevers(self):
        ...

    def plot(self):
        plt.figure(figsize=(5, 5))
        for obs in self.obstacles:
            plt.gca().add_patch(plt.Rectangle((obs[0], obs[1]), obs[2] - obs[0], obs[3] - obs[1], color='black'))
        for x, y in self.props:
            plt.plot(x, y, 'bo')
        for x, y in self.cantilevers:
            plt.plot(x, y, 'ro')

        plt.xlim(self.limits_x)
        plt.ylim(self.limits_y)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

def main():
    start_point = (0, 0)
    frame_dist = 2.4
    horizontal_dist = 0.15
    vertical_dist = 1.8
    obstacles = [(3, 3, 4, 4)]
    limits_x = [0, 10]
    limits_y = [0, 10]
    canti_dist = 0.3
    fast = Fast(start_point, frame_dist, horizontal_dist, vertical_dist, obstacles, limits_x, limits_y, canti_dist)
    fast.generate_props()
    fast.place_final_prop()
    fast.plot()

if __name__ == '__main__':
    main()
