import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon, plot_points
from shapely import LineString
from matplotlib.patches import Patch
from arch_models import *
import numpy as np
import os

class Traditional:
    def __init__(self, obstacles, shape, min_dist=0.8, canti_dist=0.3):
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

    def plot(self, sys="", name=""):
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
        ax.set_xlim([-1, 28])
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
        plt.savefig(f"out/Plot_{sys}_{name}.jpg", format="jpg", dpi=300, bbox_inches="tight")
    
    def run(self, name=""):
        os.makedirs("out", exist_ok=True)
        self.generate_props()
        self.generate_cantilevers()
        self.plot(self.__class__.__name__, name)

class Props(Traditional):
    def __init__(self, obstacles, shape, min_dist=1.5, canti_dist=0.6):
        super().__init__(obstacles, shape, min_dist, canti_dist)

class Frames(Traditional):
    def __init__(self, obstacles, shape, frame_dist=1.2, min_dist=1, vertical_dist=1, canti_dist=0.4):
        super().__init__(obstacles, shape, min_dist, canti_dist)
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
        """
        Fill the props list by scanning over a grid of candidate points using a small step.
        The grid is defined using the bounds of the shape and a step size (here 0.05).
        For each candidate point (x, y), if both (x, y) and (x + frame_dist, y) are valid and 
        the point is not inside an obstacle, they are added as props and the corresponding frame is stored.
        """
        step = 0.05

        # Get the bounds of the shape (assuming self.shape has a 'bounds' attribute: (minx, miny, maxx, maxy))
        minx, miny, maxx, maxy = 0, 0, 50, 50
        # Adjust maxx so that (x + frame_dist) stays within bounds
        maxx -= self.frame_dist

        self.props = set()
        self.frames = []

        # Create grid values for x and y
        x_values = np.arange(minx, maxx, step)
        y_values = np.arange(miny, maxy, self.vertical_dist)

        # Loop over all candidate points
        for x in x_values:
            for y in y_values:
                # Round the coordinates to 3 decimal places
                x_r, y_r = round(x, 3), round(y, 3)
                # Check if the candidate and its right neighbor (for the frame) are valid,
                # and ensure the candidate is not inside an obstacle.
                if (
                    self.is_valid_position(x_r, y_r)
                    and self.is_valid_position(x_r + self.frame_dist, y_r)
                    and not self.is_inside_obstacle(x_r, y_r)
                ):
                    # Add the candidate point and its neighbor to the props set
                    self.props.add((x_r, y_r))
                    self.props.add((round(x_r + self.frame_dist, 3), y_r))
                    # Append the corresponding frame tuple
                    self.frames.append((x_r, y_r, round(x_r + self.frame_dist, 3), y_r))

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

class Fast(Frames):
    def __init__(self, obstacles, shape, frame_dist=2.5, horizontal_dist=0.15, vertical_dist=1.8):
        super().__init__(obstacles, shape, frame_dist, horizontal_dist, vertical_dist)
        self.horizontal_dist = horizontal_dist
        self.frames = []
        self.scale = 1

    def is_valid_position(self, x, y):
        return self.shape.intersects(x, y) and not self.is_inside_obstacle(x, y) and not self.is_near_another_prop(x, y)

    def generate_props(self):
        """
        Fill the props list by scanning over a grid of candidate points using a small step.
        The grid is defined using the bounds of the shape and a step size (here 0.05).
        For each candidate point (x, y), if both (x, y) and (x + frame_dist, y) are valid and 
        the point is not inside an obstacle, they are added as props and the corresponding frame is stored.
        """
        step = 0.05

        # Get the bounds of the shape (assuming self.shape has a 'bounds' attribute: (minx, miny, maxx, maxy))
        minx, miny, maxx, maxy = 0, 0, 50, 50
        # Adjust maxx so that (x + frame_dist) stays within bounds
        maxx -= self.frame_dist

        self.props = set()
        self.frames = []

        # Create grid values for x and y
        x_values = np.arange(minx, maxx, step)
        y_values = np.arange(miny, maxy, self.vertical_dist)

        # Loop over all candidate points
        for x in x_values:
            for y in y_values:
                # Round the coordinates to 3 decimal places
                x_r, y_r = round(x, 3), round(y, 3)
                # Check if the candidate and its right neighbor (for the frame) are valid,
                # and ensure the candidate is not inside an obstacle.
                if (
                    self.is_valid_position(x_r, y_r)
                    and self.is_valid_position(x_r + self.frame_dist, y_r)
                    and not self.is_inside_obstacle(x_r, y_r)
                ):
                    # Add the candidate point and its neighbor to the props set
                    self.props.add((x_r, y_r))
                    self.props.add((round(x_r + self.frame_dist, 3), y_r))
                    # Append the corresponding frame tuple
                    self.frames.append((x_r, y_r, round(x_r + self.frame_dist, 3), y_r))



    def is_inside_obstacle(self, x, y):
        return any(obs.intersects_frame(LineString([[x, y], [x + self.frame_dist, y]])) for obs in self.obstacles)

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

    def run(self, name=""):
        os.makedirs("out", exist_ok=True)
        self.generate_props()
        self.place_final_prop()
        self.plot(self.__class__.__name__, name)

class East(Fast):
    def __init__(self, obstacles, shape, frame_dist=2.4, horizontal_dist=0.15, vertical_dist=1.8):
        super().__init__(obstacles, shape, frame_dist, horizontal_dist, vertical_dist)

def main():
    obstacles = [Obstacle(0, 0), Obstacle(2, 2)]
    villa = Villa(
        Rectangle([0, 4.75], [0, 16.3]),
        Rectangle([4.75, 9.8], [1.91, 16.3]),
        Rectangle([9.8, 15.45], [2.76, 16.3]),
        Rectangle([15.45, 23.4], [10.8, 16.3]),
        Triangle([15.45, 2.76], [15.4, 10.8], [23.4, 10.8])
    )
    for cls in [Traditional, Frames, Fast, East]:
        cls(obstacles, villa).run(cls.__name__, "test")

if __name__ == "__main__":
    main()