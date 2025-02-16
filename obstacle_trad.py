import matplotlib.pyplot as plt
from arch_models import *

class TraditionalProps:
    def __init__(self, start_point, min_dist, obstacles, shape, canti_dist):
        self.scale = 100  # Convert meters to centimeters
        self.start_point = (int(start_point[0] * self.scale), int(start_point[1] * self.scale))
        self.min_dist = int(min_dist * self.scale)
        self.canti_dist = int(canti_dist * self.scale)
        self.obstacles = [(int(x1 * self.scale), int(y1 * self.scale), int(x2 * self.scale), int(y2 * self.scale)) for x1, y1, x2, y2 in obstacles]
        self.shape = shape
        self.props = []
        self.cantilevers = []

    def is_inside_obstacle(self, x, y):
        for obs in self.obstacles:
            if obs[0] < x < obs[2] and obs[1] < y < obs[3]:
                return True
        return False

    def is_valid_position(self, x, y):
        if not self.shape.is_inside(x / self.scale, y / self.scale) or self.is_inside_obstacle(x, y):
            return False
        return True

    def generate_props(self):
        self.props = []
        for x in range(0, 100 * self.scale + 1, self.min_dist):
            for y in range(0, 100 * self.scale + 1, self.min_dist):
                if self.is_valid_position(x, y):
                    self.props.append((x, y))

    def generate_cantilevers(self):
        canti_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        canti_directions.extend([(x * i, y * i) for x, y in canti_directions for i in [1, 2]])
        no_prop = lambda x, y: (x, y) not in self.props
        normalize = lambda x: 0 if x == 0 else x // abs(x)

        for x, y in self.props:
            for dx, dy in canti_directions:
                new_x, new_y = x + dx * self.canti_dist, y + dy * self.canti_dist
                if no_prop(x + normalize(dx) * self.min_dist, y + normalize(dy) * self.min_dist) and \
                   self.is_edge_position(new_x, new_y, dx, dy):
                    self.cantilevers.append((new_x, new_y))

    def is_edge_position(self, x, y, dx, dy):
        def is_near_obstacle():
            for obs in self.obstacles:
                if dx == 0:
                    if abs(y - obs[1]) < self.canti_dist or abs(y - obs[3]) < self.canti_dist:
                        return True
                elif dy == 0:
                    if abs(x - obs[0]) < self.canti_dist or abs(x - obs[2]) < self.canti_dist:
                        return True
            return False

        return (self.shape.limited(x / self.scale, y / self.scale, dx, dy, self.canti_dist / self.scale) or is_near_obstacle()) and self.is_valid_position(x, y)

    def plot_props_and_obstacles(self):
        plt.figure(figsize=(5, 5))
        ax = plt.gca()

        for x, y in self.props:
            ax.plot(x / self.scale, y / self.scale, 'bo')

        for x, y in self.cantilevers:
            ax.plot(x / self.scale, y / self.scale, 'go')

        for (obs_x1, obs_y1, obs_x2, obs_y2) in self.obstacles:
            rect = plt.Rectangle((obs_x1 / self.scale, obs_y1 / self.scale), (obs_x2 - obs_x1) / self.scale, (obs_y2 - obs_y1) / self.scale, fill=True, color='red', alpha=0.5)
            ax.add_patch(rect)

        ax.set_xlim([-1, 30])
        ax.set_ylim([-1, 30])
        ax.set_title("Prop Placement with Obstacle Avoidance")
        ax.set_xlabel("X coordinate")
        ax.set_ylabel("Y coordinate")
        plt.grid(True)
        plt.show()


def main():
    start_point = (0, 0)
    min_dist = 0.8
    obstacles = [(0, 0, 1, 1), (2, 2, 3, 3), (7, 7, 8, 8)]
    l_shape = L_shape(Rectangle([0, 15], [0, 13]), Rectangle([15, 25], [0, 6.5]))
    rect = Rectangle([0, 15], [0, 15])
    t_shape = T_shape(Rectangle([0, 15], [8, 20]), Rectangle([5, 10], [0, 8]))
    circle = Torus(19.38 / 2, 5 / 2)
    villa = Villa(
        Rectangle([0, 4.75], [0, 16.3]),
        Rectangle([4.75, 9.8], [1.91, 16.3]),
        Rectangle([9.8, 15.45], [2.76, 16.3]),
        Rectangle([15.45, 23.4], [10.8, 16.3]),
        Triangle([15.45, 2.76], [15.4, 10.8], [23.4, 10.8])
    )
    canti_dist = 0.3

    props_system = TraditionalProps(start_point, min_dist, obstacles, villa, canti_dist)
    props_system.generate_props()
    props_system.generate_cantilevers()
    props_system.plot_props_and_obstacles()

if __name__ == '__main__':
    main()
