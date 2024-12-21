import matplotlib.pyplot as plt

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


def main():
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

if __name__ == '__main__':
    main()
