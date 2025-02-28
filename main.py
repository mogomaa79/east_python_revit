from obstacles import *
import csv

def load_obstacles(building):
    obstacles = []
    with open("data/obstacles/" + building) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obstacles.append(Obstacle(float(row['x']), float(row['y'])))
    return obstacles

def load_shapes():
    shapes = {
        "Rectangular": {},
        "Circular": {},
        "L-shape": {},
        "T-shape": {},
        "Villa": {},
    }
    for shape in os.listdir("data/buildings"):
        if shape.endswith(".csv"):
            with open("data/buildings/" + shape) as csvfile:
                reader = csv.reader(csvfile)
                if shape.startswith("Rect"):
                    for row in reader:
                        shapes[shape[:-4]][row[0]] = Rectangle([float(row[1]), float(row[3])], [float(row[2]), float(row[4])])
                elif shape.startswith("L-s") or shape.startswith("T-s"):
                    for row in reader:
                        rect1 = Rectangle([float(row[1]), float(row[3])], [float(row[2]), float(row[4])])
                        rect2 = Rectangle([float(row[5]), float(row[7])], [float(row[6]), float(row[8])])
                        shapes[shape[:-4]][row[0]] = L_shape(rect1, rect2)
                elif shape.startswith("Circular"):
                    for row in reader:
                        shapes[shape[:-4]][row[0]] = Torus(float(row[1]), float(row[2]))
                elif shape.startswith("Villa"):
                    for row in reader:
                        rect1 = Rectangle([float(row[1]), float(row[3])], [float(row[2]), float(row[4])])
                        rect2 = Rectangle([float(row[5]), float(row[7])], [float(row[6]), float(row[8])])
                        rect3 = Rectangle([float(row[9]), float(row[11])], [float(row[10]), float(row[12])])
                        rect4 = Rectangle([float(row[13]), float(row[15])], [float(row[14]), float(row[16])])
                        tri = Triangle([float(row[17]), float(row[18])], [float(row[19]), float(row[20])], [float(row[21]), float(row[22])])
                        shapes[shape[:-4]][row[0]] = Villa(rect1, rect2, rect3, rect4, tri)
    return shapes

def main():
    buildings = os.listdir("data/obstacles")
    shapes = load_shapes()
    for building in buildings:
        if building.endswith(".csv"):
            obstacles = load_obstacles(building)
            model, size = building[:-4].split()
            shape = shapes[model][size]
            for cls in [Traditional, Props, Frames, Fast, East]:
                cls(obstacles, shape).run(building[:-4])
            break

if __name__ == "__main__":
    main()