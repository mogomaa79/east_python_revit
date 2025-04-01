import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon, plot_points
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
        self.props = set()
        self.cantilevers = set()
        self.frames = set()

    def is_inside_obstacle(self, x, y):
        return any(
            obs.intersects(x / self.scale, y / self.scale) for obs in self.obstacles
        )

    def is_valid_position(self, x, y):
        return self.shape.intersects(
            x / self.scale, y / self.scale
        ) and not self.is_inside_obstacle(x, y)

    def generate_props(self):
        """Generate valid prop positions using NumPy meshgrid for efficiency."""
        x_vals = np.arange(0, 100 * self.scale + 1, self.min_dist)
        y_vals = np.arange(0, 100 * self.scale + 1, self.min_dist)
        grid_x, grid_y = np.meshgrid(x_vals, y_vals)
        points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

        self.props = {(x, y) for x, y in points if self.is_valid_position(x, y)}

    def generate_cantilevers(self):
        canti_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        no_prop = lambda x, y: (x, y) not in self.props
        normalize = lambda x: 0 if x == 0 else x // abs(x)

        for x, y in self.props:
            for dx, dy in canti_directions:
                new_x, new_y = x + dx * self.canti_dist, y + dy * self.canti_dist
                if no_prop(
                    x + normalize(dx) * self.min_dist, y + normalize(dy) * self.min_dist
                ) and self.is_edge_position(new_x, new_y, dx, dy):
                    self.cantilevers.add((new_x, new_y))

    def is_edge_position(self, x, y, dx, dy):
        def is_near_obstacle():
            return any(
                obs.limited(
                    x / self.scale, y / self.scale, dx, dy, self.canti_dist / self.scale
                )
                for obs in self.obstacles
            )

        return (
            self.shape.limited(
                x / self.scale, y / self.scale, dx, dy, self.canti_dist / self.scale
            )
            or is_near_obstacle()
        ) and self.is_valid_position(x, y)

    def plot(self, sys="", name=""):
        """Plot obstacles, props, and cantilevers with improved visuals."""
        fig, ax = plt.subplots(figsize=(15, 7.5))

        # Plot obstacles
        for obs in self.obstacles:
            plot_polygon(
                obs.polygon,
                ax=ax,
                facecolor="red",
                edgecolor="black",
                alpha=0.6,
                linewidth=1.2,
                add_points=False,
            )

        # Plot props
        if self.props:
            prop_points = [Point(x / self.scale, y / self.scale) for x, y in self.props]
            plot_points(
                prop_points, ax=ax, marker="o", color="blue", markersize=4, alpha=0.8
            )

        # Plot cantilevers
        if self.cantilevers:
            canti_points = [
                Point(x / self.scale, y / self.scale) for x, y in self.cantilevers
            ]
            plot_points(
                canti_points, ax=ax, marker="o", color="green", markersize=4, alpha=0.8
            )

        # Improve plot aesthetics
        max_x = max(self.props | self.cantilevers, key=lambda x: x[0])[0] / self.scale
        max_y = max(self.props | self.cantilevers, key=lambda x: x[1])[1] / self.scale
        ax.set_xlim([-1, max_x + 4])
        ax.set_ylim([-1, max_y + 4])
        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

        # Legend for clarity
        legend_patches = [
            Patch(facecolor="red", edgecolor="black", alpha=0.5, label="Obstacles"),
            Patch(color="blue", label="Props"),
            Patch(color="green", label="Cantilevers"),
        ]
        ax.legend(handles=legend_patches, loc="upper right", fontsize=10)
        plt.savefig(
            f"out/Plot_{sys}_{name}.jpg", format="jpg", dpi=300, bbox_inches="tight"
        )
        plt.close()

    def run(self, name=""):
        os.makedirs("out", exist_ok=True)
        done = os.listdir("out")
        if "Plot_" + self.__class__.__name__ + "_" + name + ".jpg" in done:
            return 0, 0, 0, self.__class__.__name__
        self.generate_props()
        self.generate_cantilevers()
        self.plot(self.__class__.__name__, name)
        return (
            len(self.props) - len(self.frames) * 2,
            len(self.cantilevers),
            len(self.frames),
            self.__class__.__name__,
        )


class Props(Traditional):
    def __init__(self, obstacles, shape, min_dist=1.5, canti_dist=0.6):
        super().__init__(obstacles, shape, min_dist, canti_dist)


class Frames(Traditional):
    def __init__(
        self,
        obstacles,
        shape,
        frame_dist=1,
        min_dist=1,
        vertical_dist=1,
        last_prop_dist=0.6,
    ):
        super().__init__(obstacles, shape, min_dist)
        self.frame_dist = frame_dist
        self.scale = 1
        self.min_dist = min_dist
        self.vertical_dist = vertical_dist
        self.horizontal_dist = min_dist
        self.last_prop_dist = last_prop_dist

    def is_inside_obstacle(self, x, y):
        return any(
            obs.intersects_frame(x, x + self.frame_dist, y) for obs in self.obstacles
        )

    def is_valid_position(self, x, y):
        return (
            self.shape.intersects(x, y)
            and self.shape.intersects(x + self.frame_dist, y)
            and not self.is_inside_obstacle(x, y)
            and not self.is_near_another_prop(x, y)
            and not self.is_near_another_prop(x + self.frame_dist, y)
            and not self.is_between_frame(x, y)
            and not self.is_between_frame(x + self.frame_dist, y)
        )

    def is_valid_prop(self, x, y):
        return super().is_valid_position(x, y) and not self.is_between_frame(x, y)

    def is_between_frame(self, x, y):
        for frame in self.frames:
            if frame[0] < x < frame[2] and frame[1] == y:
                return True
        return False

    def is_near_another_prop(self, x, y, epsilon=1e-2):
        """Check if (x, y) is near an existing prop within defined horizontal and vertical distances."""
        for prop in self.props:
            if (
                abs(prop[0] - x) + epsilon < self.horizontal_dist
                and abs(prop[1] - y) + epsilon < self.vertical_dist
            ):
                return True
        return False

    def generate_props(self):
        """
        Fill the props list by scanning over a grid of candidate points using a small step.
        The grid is defined using the bounds of the shape and a step size (here 0.05).
        For each candidate point (x, y), if both (x, y) and (x + frame_dist, y) are valid and
        the point is not inside an obstacle, they are added as props and the corresponding frame is stored.
        """
        minx, miny, maxx, maxy = 0.4, 0.01, 50, 50

        maxx -= self.frame_dist

        self.props = set()
        self.frames = []

        # Create grid values for x and y
        x_values = np.arange(minx, maxx, self.horizontal_dist)
        y_values = np.arange(miny, maxy, self.vertical_dist)

        # Loop over all candidate points
        for x in x_values:
            for y in y_values:
                # Round the coordinates to 3 decimal places
                x_r, y_r = round(x, 3), round(y, 3)
                while self.is_inside_obstacle(x_r, y_r):
                    x_r += 0.05
                if self.is_valid_position(x_r, y_r):
                    # Add the candidate point and its neighbor to the props set
                    self.props.add((x_r, y_r))
                    self.props.add((round(x_r + self.frame_dist, 3), y_r))
                    # Append the corresponding frame tuple
                    self.frames.append((x_r, y_r, round(x_r + self.frame_dist, 3), y_r))

    def buffer_contains_prop(self, x, y):
        buffer = Point(x, y).buffer(1)
        for prop in self.props:
            if buffer.intersects(Point(prop[0], prop[1])):
                return False
        return True
    
    def place_final_prop(self):
        """If there is a gap after the last frame in any direction.
        Fill the gap with a prop in the midpoint till the edge."""
        x_vals, y_vals = {}, {}
        for x, y in self.props:
            if x not in x_vals:
                x_vals[x] = (400, -1)
            if y not in y_vals:
                y_vals[y] = (400, -1)
            x_vals[x] = (min(x_vals[x][0], y), max(x_vals[x][1], y))
            y_vals[y] = (min(y_vals[y][0], x), max(y_vals[y][1], x))
        
        for x in x_vals:
            if x_vals[x][0] != -1:   
                edge = False 
                for diff in [i/10 for i in range(15, int(self.last_prop_dist * 10), -1)]:
                    new_y = x_vals[x][0] - diff
                    if not self.shape.intersects(x, new_y):
                        edge = True
                    if edge:
                        if self.is_valid_prop(x, new_y):
                            self.props.add((x, new_y))
                            break
                    else:
                        if not edge and self.buffer_contains_prop(x, new_y) and self.is_valid_prop(x, new_y):
                            self.props.add((x, new_y))
                            break

            if x_vals[x][1] != -1:
                edge = False
                for diff in [i/10 for i in range(15, int(self.last_prop_dist * 10), -1)]:
                    new_y = x_vals[x][1] + diff
                    if not self.shape.intersects(x, new_y):
                        edge = True
                    if edge:
                        if self.is_valid_prop(x, new_y):
                            self.props.add((x, new_y))
                            break
                    else:
                        if not edge and self.buffer_contains_prop(x, new_y) and self.is_valid_prop(x, new_y):
                            self.props.add((x, new_y))
                            break
        for y in y_vals:
            if y_vals[y][0] != -1:
                edge = False
                for diff in [i/10 for i in range(15, int(self.last_prop_dist * 10), -1)]:
                    new_x = y_vals[y][0] - diff
                    if not self.shape.intersects(new_x, y):
                        edge = True
                    if edge:
                        if self.is_valid_prop(new_x, y):
                            self.props.add((new_x, y))
                            break
                    else:
                        if not edge and self.buffer_contains_prop(new_x, y) and self.is_valid_prop(new_x, y):
                            self.props.add((new_x, y))
                            break
            if y_vals[y][1] != -1:
                edge = False
                for diff in [i/10 for i in range(15, int(self.last_prop_dist * 10), -1)]:
                    new_x = y_vals[y][1] + diff
                    if not self.shape.intersects(new_x, y):
                        edge = True
                    if edge:
                        if self.is_valid_prop(new_x, y):
                            self.props.add((new_x, y))
                            break
                    else:
                        if not edge and self.buffer_contains_prop(new_x, y) and self.is_valid_prop(new_x, y):
                            self.props.add((new_x, y))
                            break
        
    # def place_final_prop(self):
    #     for x, y in self.props.copy():
    #        for diff in [i/10 for i in range(15, int(self.last_prop_dist * 10), -1)]:
    #             new_x = x + diff
    #             if self.buffer_contains_prop(new_x, y) and self.is_valid_prop(new_x, y):
    #                 self.props.add((new_x, y))
    #             new_x = x - diff
    #             if self.buffer_contains_prop(new_x, y) and self.is_valid_prop(new_x, y):
    #                 self.props.add((new_x, y))
    #             new_y = y + diff
    #             if self.buffer_contains_prop(x, new_y) and self.is_valid_prop(x, new_y):
    #                 self.props.add((x, new_y))
    #             new_y = y - diff
    #             if self.buffer_contains_prop(x, new_y) and self.is_valid_prop(x, new_y):
    #                 self.props.add((x, new_y))
    

    def run(self, name=""):
        os.makedirs("out", exist_ok=True)
        done = os.listdir("out")
        if "Plot_" + self.__class__.__name__ + "_" + name + ".jpg" in done:
            return 0, 0, 0, self.__class__.__name__
        self.generate_props()
        self.place_final_prop()
        self.plot(self.__class__.__name__, name)
        return (
            len(self.props) - len(self.frames) * 2,
            len(self.cantilevers),
            len(self.frames),
            self.__class__.__name__,
        )
class Fast(Frames):
    def __init__(
        self, obstacles, shape, frame_dist=2.5, horizontal_dist=0.15, vertical_dist=1.8, last_prop_dist=0.2
    ):
        super().__init__(obstacles, shape, frame_dist, horizontal_dist, vertical_dist, last_prop_dist)
        self.horizontal_dist = horizontal_dist
        self.frames = []
        self.scale = 1


class East(Fast):
    def __init__(
        self, obstacles, shape, frame_dist=2.4, horizontal_dist=0.15, vertical_dist=1.8, last_prop_dist=0.2
    ):
        super().__init__(obstacles, shape, frame_dist, horizontal_dist, vertical_dist, last_prop_dist)


def main():
    obstacles = [
        Obstacle(0, 0),
        Obstacle(4.1, 0),
        Obstacle(0, 2.322),
        Obstacle(0, 5.614),
        Obstacle(0, 8.91),
        Obstacle(0, 13.11),
        Obstacle(2.84, 13.11),
        Obstacle(6.01, 13.11),
        Obstacle(8.51, 13.11),
        Obstacle(11.282, 13.11),
        Obstacle(13.832, 13.11),
        Obstacle(16.58, 13.11),
        Obstacle(20.472, 13.11),
        Obstacle(6.01, 10.41),
        Obstacle(2.995, 8.91),
        Obstacle(8.51, 8.91),
        Obstacle(11.282, 8.91),
        Obstacle(14.237, 8.91),
        Obstacle(20.167, 9.21),
        Obstacle(16.369, 5.112),
        Obstacle(8.421, 1.631),
        Obstacle(13.334, 2.378),
        Obstacle(4.41, 6.51),
        Obstacle(8.51, 6.51),
        Obstacle(11.282, 6.51),
    ]

    villa = Villa(
        Rectangle([0, 4.44], [0, 13.58]),
        Rectangle([4.44, 8.76], [1.64, 13.58]),
        Rectangle([8.76, 13.611], [2.37, 13.58]),
        Rectangle([13.611, 20.48], [9.239, 13.58]),
        Triangle([13.611, 9.239], [20.48, 9.239], [13.611, 2.37]),
    )
    import shutil
    shutil.rmtree("out")
    for cls in [Traditional, Frames, Props, Fast, East]:
        print(cls(obstacles, villa).run("test"))


if __name__ == "__main__":
    main()
