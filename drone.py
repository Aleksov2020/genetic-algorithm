import random


class Drone:

    def __init__(self, base, load_capacity):
        self.load_capacity = load_capacity
        self.start_vertex = base
        self.end_vertex = base
        self.chromosome = []
        self.length_route = 0
        self.weight = 0

        self.penalty_weight_value = 100000

    def shuffle_gen(self):
        random.shuffle(self.chromosome)

    def set_route_length(self):
        self.length_route = self.start_vertex.distance(self.chromosome[0])

        for i in range(len(self.chromosome) - 1):
            self.length_route += self.chromosome[i].distance(self.chromosome[i + 1])

        self.length_route += self.chromosome[len(self.chromosome) - 1].distance(self.end_vertex)

    def set_route_weight_and_penalty(self):
        for i in range(len(self.chromosome)):
            self.weight += self.chromosome[i].weight
            if self.weight > self.load_capacity:
                self.length_route += self.penalty_weight_value

            if self.chromosome[i].x_coordinate == self.start_vertex.x_coordinate and self.chromosome[
                i].y_coordinate == self.start_vertex.y_coordinate:
                self.weight = 0

    def swap_gens(self, first_gen_i, sec_gen_i):
        self.chromosome[first_gen_i], self.chromosome[sec_gen_i] = self.chromosome[sec_gen_i], self.chromosome[
            first_gen_i]
