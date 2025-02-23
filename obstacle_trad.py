import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon, plot_points
from matplotlib.patches import Patch
from arch_models import *
import numpy as np

class TraditionalProps:
    def __init__(self, min_dist, obstacles, shape, canti_dist):
        self.scale = 100  # Convert meters to centimeters
        self.start_point = (0, 0)
        self.min_dist = int(min_dist * self.scale)
        self.canti_dist = int(canti_dist * self.scale)
        self.obstacles = obstacles
        self.shape = shape
        self.props = []
        self.cantilevers = []

    def is_inside_obstacle(self, x, y):
        return any(obs.intersects(x / self.scale, y / self.scale) for obs in self.obstacles)

    def is_valid_position(self, x, y):
        return self.shape.intersects(x / self.scale, y / self.scale) and not self.is_inside_obstacle(x, y)

    def generate_props(self):
        """Generate valid prop positions using NumPy meshgrid for efficiency."""
        x_vals = np.arange(0, 100 * self.scale + 1, self.min_dist)
        y_vals = np.arange(0, 100 * self.scale + 1, self.min_dist)
        grid_x, grid_y = np.meshgrid(x_vals, y_vals)
        points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

        self.props = [(x, y) for x, y in points if self.is_valid_position(x, y)]

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
            return any(obs.limited(x / self.scale, y / self.scale, dx, dy, self.canti_dist / self.scale) for obs in self.obstacles)

        return (self.shape.limited(x / self.scale, y / self.scale, dx, dy, self.canti_dist / self.scale) or is_near_obstacle()) and self.is_valid_position(x, y)

    def plot(self):
        """Plot obstacles, props, and cantilevers with improved visuals."""
        fig, ax = plt.subplots(figsize=(15, 7.5))

        # Plot obstacles
        for obs in self.obstacles:
            plot_polygon(obs.polygon, ax=ax, facecolor='red', edgecolor='black', alpha=0.6, linewidth=1.2, add_points=False)

        # Plot props
        if self.props:
            prop_points = [Point(x / self.scale, y / self.scale) for x, y in self.props]
            plot_points(prop_points, ax=ax, marker='o', color='blue', markersize=4, alpha=0.8)

        # Plot cantilevers
        if self.cantilevers:
            canti_points = [Point(x / self.scale, y / self.scale) for x, y in self.cantilevers]
            plot_points(canti_points, ax=ax, marker='o', color='green', markersize=4, alpha=0.8)

        # Improve plot aesthetics
        ax.set_xlim([-1, 24])
        ax.set_ylim([-1, 20])
        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

        # Legend for clarity
        legend_patches = [
            Patch(facecolor='red', edgecolor='black', alpha=0.5, label="Obstacles"),
            Patch(color='blue', label="Props"),
            Patch(color='green', label="Cantilevers")
        ]
        ax.legend(handles=legend_patches, loc="upper right", fontsize=10)

        plt.show()

def main():
    min_dist = 0.8
    obstacles = [Obstacle(0, 0), Obstacle(2, 2), Obstacle(7, 7)]
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

    props_system = TraditionalProps(min_dist, obstacles, villa, canti_dist)
    props_system.generate_props()
    props_system.generate_cantilevers()
    props_system.plot()

if __name__ == '__main__':
    main()
