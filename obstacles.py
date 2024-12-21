import matplotlib.pyplot as plt

class East:
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

def run_east():
    start_point = (0, 0)
    frame_dist = 2.4
    horizontal_dist = 0.15
    vertical_dist = 1.8
    obstacles = [(3, 3, 4, 4)]
    limits_x = [0, 10]
    limits_y = [0, 10]
    canti_dist = 0.3
    east = East(start_point, frame_dist, horizontal_dist, vertical_dist, obstacles, limits_x, limits_y, canti_dist)
    east.generate_props()
    east.place_final_prop()
    east.plot()

class TraditionalProps:
    def __init__(self, start_point, min_dist, obstacles, limits_x, limits_y, canti_dist):
        self.start_point = start_point
        self.min_dist = min_dist
        self.obstacles = obstacles
        self.limits_x = limits_x
        self.limits_y = limits_y
        self.canti_dist = canti_dist
        self.props = []
        self.cantilevers = []

    def is_inside_obstacle(self, x, y):
        for obs in self.obstacles:
            if obs[0] < x < obs[2] and obs[1] < y < obs[3]:
                return True
        return False

    def is_valid_position(self, x, y):
        if (x < self.limits_x[0] or x > self.limits_x[1] or
            y < self.limits_y[0] or y > self.limits_y[1] or
            self.is_inside_obstacle(x, y)):
            return False
        return True

    def generate_props(self):
        start_point = self.start_point
        while not self.is_valid_position(*start_point):
            start_point = (start_point[0] + 1, start_point[1])
        self.props = [start_point]
        directions = [(self.min_dist, 0), (-self.min_dist, 0), (0, self.min_dist), (0, -self.min_dist)]

        # Initial loop to populate grid with props
        queue = [start_point]
        while queue:
            current_x, current_y = queue.pop(0)
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if self.is_valid_position(new_x, new_y):
                    if (new_x, new_y) not in self.props:
                        self.props.append((new_x, new_y))
                        queue.append((new_x, new_y))

    def plot_cantilevers(self):
        canti_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        canti_directions.extend([(x * i, y * i) for x, y in canti_directions for i in range(2, 6)])
        no_prop = lambda x, y: (x, y) not in self.props
        normalize = lambda x: 0 if x == 0 else x // abs(x)

        for x, y in self.props:
            for dx, dy in canti_directions:
                new_x, new_y = x + dx * self.canti_dist, y + dy * self.canti_dist
                if no_prop(x + normalize(dx) * self.min_dist, y + normalize(dy) * self.min_dist) and \
                   self.is_edge_position(new_x, new_y, dx, dy):
                    self.cantilevers.append((new_x, new_y))

    def is_edge_position(self, x, y, dx, dy):
        def limited():
            if dx == 0:
                return abs(y - self.limits_y[0]) < self.canti_dist or abs(y - self.limits_y[1]) < self.canti_dist
            elif dy == 0:
                return abs(x - self.limits_x[0]) < self.canti_dist or abs(x - self.limits_x[1]) < self.canti_dist
            return False

        def is_near_obstacle():
            for obs in self.obstacles:
                if dx == 0:
                    if abs(y - obs[1]) < self.canti_dist or abs(y - obs[3]) < self.canti_dist:
                        return True
                elif dy == 0:
                    if abs(x - obs[0]) < self.canti_dist or abs(x - obs[2]) < self.canti_dist:
                        return True
            return False

        return (limited() or is_near_obstacle()) and self.is_valid_position(x, y)

    def plot_props_and_obstacles(self):
        plt.figure(figsize=(5, 5))
        ax = plt.gca()

        # Plot props
        for x, y in self.props:
            ax.plot(x, y, 'bo')  # Prop as blue dot

        for x, y in self.cantilevers:
            ax.plot(x, y, 'ro')

        # Plot obstacles
        for (obs_x1, obs_y1, obs_x2, obs_y2) in self.obstacles:
            rect = plt.Rectangle((obs_x1, obs_y1), obs_x2 - obs_x1, obs_y2 - obs_y1, fill=True, color='red', alpha=0.5)
            ax.add_patch(rect)

        # Set plot limits
        ax.set_xlim([self.limits_x[0] - 2, self.limits_x[1] + 2])
        ax.set_ylim([self.limits_y[0] - 2, self.limits_y[1] + 2])
        ax.set_title("Prop Placement with Obstacle Avoidance")
        ax.set_xlabel("X coordinate")
        ax.set_ylabel("Y coordinate")
        plt.grid(True)
        plt.show()

def run_traditional():
    # Example Usage
    start_point = (0, 0)
    min_dist = 1.5
    obstacles = [(0, 0, 1, 1), (2, 2, 3, 3), (7, 7, 8, 8)]
    limits_x = (0, 10)
    limits_y = (0, 10)
    canti_dist = 0.3

    # Create instance
    props_system = TraditionalProps(start_point, min_dist, obstacles, limits_x, limits_y, canti_dist)

    # Generate props and cantilevers
    props_system.generate_props()
    props_system.plot_cantilevers()

    # Plot props and obstacles
    props_system.plot_props_and_obstacles()

class Frames:
    def __init__(self, start_point, frame_dist, horizontal_dist, vertical_dist, obstacles, limits_x, limits_y, canti_dist):
        self.start_point = start_point
        self.frame_dist = frame_dist
        self.obstacles = obstacles
        self.limits_x = limits_x
        self.limits_y = limits_y
        self.canti_dist = canti_dist
        self.horizontal_dist = horizontal_dist
        self.vertical_dist = vertical_dist
        self.props = []
        self.cantilevers = []

    def generate_props(self):
        """Fill the props list with the props generated. 
        Distance in horizontal and vertical are defined by the user.
        Frames dist is the distance between two props in the frame"""
        x, y = self.start_point
        while not self.is_valid_position(x, y) or not self.is_valid_position(x + self.frame_dist, y):
            x += 0.1
        x, y = round(x, 2), round(y, 2)
        self.props = [(x, y), (x + self.frame_dist, y)]
        directions = [(self.horizontal_dist, 0), (-self.horizontal_dist, 0), (0, self.vertical_dist), (0, -self.vertical_dist)]
        queue = [(x, y)]
        visited = set(queue)

        while queue:
            current_x, current_y = queue.pop(0)
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if (new_x, new_y) not in visited and self.is_valid_position(new_x, new_y) and self.is_valid_position(new_x + self.frame_dist, new_y):
                    new_x, new_y = round(new_x, 2), round(new_y, 2)
                    self.props.append((new_x, new_y))
                    self.props.append((new_x + self.frame_dist, new_y))
                    queue.append((new_x, new_y))
                    queue.append((new_x + self.frame_dist, new_y))
                    visited.add((new_x, new_y))
                    visited.add((new_x + self.frame_dist, new_y))

    def is_inside_obstacle(self, x, y):
        for obs in self.obstacles:
            if obs[0] < x < obs[2] and obs[1] < y < obs[3]:
                return True
        return False

    def is_valid_position(self, x, y):
        if (x < self.limits_x[0] or x > self.limits_x[1] or
            y < self.limits_y[0] or y > self.limits_y[1] or
            self.is_inside_obstacle(x, y)) or self.is_near_another_prop(x, y):
            return False
        return True

    def is_near_another_prop(self, x, y):
        for prop in self.props:
            if abs(prop[0] - x) < self.horizontal_dist and abs(prop[1] - y) < self.vertical_dist:
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
            if x == max_x and (dist := self.limits_x[1] - max_x):
                if dist >= self.canti_dist:
                    self.cantilevers.append((max_x + self.canti_dist, y))
                if dist > self.canti_dist:
                    self.props.append((self.limits_x[1], y))
            if x == min_x and (dist := min_x - self.limits_x[0]):
                if dist >= self.canti_dist:
                    self.cantilevers.append((min_x - self.canti_dist, y))
                if dist > self.canti_dist:
                    self.props.append((self.limits_x[0], y))
            
            if y == max_y and (dist := self.limits_y[1] - max_y):
                if dist >= self.canti_dist:
                    self.cantilevers.append((x, max_y + self.canti_dist))
                if dist > self.canti_dist:
                    self.props.append((x, self.limits_y[1]))
            
            if y == min_y and (dist := min_y - self.limits_y[0]):
                if dist >= self.canti_dist:
                    self.cantilevers.append((x, min_y - self.canti_dist))
                if dist > self.canti_dist:
                    self.props.append((x, self.limits_y[0]))

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

def run_frames():
    start_point = (0, 0)
    frame_dist = 1.2
    horizontal_dist = 1
    vertical_dist = 1
    obstacles = [(3, 3, 4, 4)]
    limits_x = [0, 5]
    limits_y = [0, 5]
    canti_dist = 0.4
    frames = Frames(start_point, frame_dist, horizontal_dist, vertical_dist, obstacles, limits_x, limits_y, canti_dist)
    frames.generate_props()
    frames.generate_cantilevers()
    frames.plot()

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

def run_fast():
    start_point = (0, 0)
    frame_dist = 2.5
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


def main():
    system = input("Choose a system to run: 1. East, 2. Traditional, 3. Frames, 4. Fast: ")
    if system == "1":
        run_east()
    elif system == "2":
        run_traditional()
    elif system == "3":
        run_frames()
    elif system == "4":
        run_fast()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()