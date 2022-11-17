import math


class Vertex:
    def __init__(self, x_coordinate, y_coordinate, weight, index):
        self.index = index
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.weight = weight
        self.default_color = (0, 0, 0)
        self.default_size = 5

    def distance(self, vertex_to):
        return math.sqrt(math.sqrt((self.x_coordinate - vertex_to.x_coordinate) ** 2 + (self.y_coordinate - vertex_to.y_coordinate) ** 2))

