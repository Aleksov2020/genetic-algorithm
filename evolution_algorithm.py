import itertools
import random

import vertex
import drone
import pygame

import time
import matplotlib.pyplot as plt


def transform_route(route):
    result = ""
    flag = False
    for v in route:
        if v.index != 0:
            flag = False
            result += str(v.index) + " -> "
        if v.index == 0 and not (flag):
            flag = True
            result += str(v.index) + "\n"
    return result


def print_vertexes(vertexes_to_print):
    for v in vertexes_to_print:
        print("====================")
        # print("x = " + str(v.x_coordinate))
        # print("y = " + str(v.y_coordinate))
        # print("weight = " + str(v.weight))
        print("index = " + str(v.index))


class EvolutionAlgorithm:

    def __init__(self, population, swap_count):
        self.load_capacity = 5
        self.population = population
        self.vertexes = []
        self.weight_sum = 0
        self.drone_min_num = 0

        self.drone_entity_list = []

        self.entity_with_one_swap_mutation = swap_count // 2
        self.entity_with_two_swap_mutation = swap_count // 2
        self.random_entity_count = int(population - swap_count - 1)
        self.min_route_count = 1

    def set_vertexes(self, vertex_x_coordinate, vertex_y_coordinate, vertex_weight, vertex_index):
        self.vertexes.append(
            vertex.Vertex(
                vertex_x_coordinate,
                vertex_y_coordinate,
                vertex_weight,
                vertex_index
            )
        )

    def print_drones(self):
        print("Drones count : " + str(len(self.drone_entity_list)))
        for d in self.drone_entity_list:
            print("--------------")
            print(d.length_route)
            print_vertexes(d.chromosome)

    def set_load_capacity(self):
        s = 0
        for v in self.vertexes:
            s += v.weight

        self.weight_sum = s

    def set_drone_min_num(self):
        self.drone_min_num = len(self.vertexes)

    def set_drones_chromosome(self, base):
        self.drone_entity_list = []
        for i in range(self.population):
            drone_entity = drone.Drone(base, self.load_capacity)
            drone_entity.chromosome = list(self.vertexes)
            for j in range(self.drone_min_num):
                drone_entity.chromosome.append(base)

            self.drone_entity_list.append(drone_entity)

    def draw_gui(self, screen, bg, base):
        # INSIDE THE GAME LOOP
        screen.blit(bg, (0, 0))
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw a solid red point. This is our base
        pygame.draw.circle(screen, base.default_color, (base.x_coordinate, base.y_coordinate), base.default_size)

        base_label = pygame.font.Font(None, 22).render(str("BASE"), 1, (0, 0, 0))
        screen.blit(base_label, (base.x_coordinate - 20, base.y_coordinate + 12))

        # Draw a solid black point. This is our vertexes
        for v in self.vertexes:
            pygame.draw.circle(
                screen,
                v.default_color,
                (v.x_coordinate, v.y_coordinate),
                v.default_size)

            vertex_weight_label = pygame.font.Font(None, 20).render(str(v.weight), 1, (0, 0, 0))
            screen.blit(vertex_weight_label, (v.x_coordinate - 5, v.y_coordinate - 22))

    def run(self, base):
        # run process
        pygame.init()

        # Set up the drawing window
        screen = pygame.display.set_mode([1500, 900])
        bg = pygame.image.load("background-map.jpg")

        running = True
        generation = 0
        equal_counter = 0

        while running:
            generation += 1
            self.draw_gui(screen, bg, base)

            if generation == 1:
                # first gen
                last_min = -1
                for d in self.drone_entity_list:
                    d.shuffle_gen()
                    d.set_route_length()
                    d.set_route_weight_and_penalty()
            else:
                last_min = min_
                # clusters
                # [minimal chromosome] [random chromosome] [one swap chromosome] [two swap chromosome]
                #           1                   5999                 2000                2000
                # set random chromosome
                for i in range(self.min_route_count, self.random_entity_count):
                    self.drone_entity_list[i].shuffle_gen()

                # set one-swap mutation
                chrom_before_i = self.min_route_count + self.random_entity_count
                chrom_after_i = chrom_before_i + self.entity_with_one_swap_mutation

                for i in range(chrom_before_i, chrom_after_i):
                    # take minimal chromosome
                    self.drone_entity_list[i].chromosome = list(min_chromosome)
                    # swap two random gens
                    first_pos = random.randint(0, len(self.drone_entity_list[i].chromosome) - 1)
                    sec_pos = random.randint(0, len(self.drone_entity_list[i].chromosome) - 1)
                    self.drone_entity_list[i].swap_gens(first_pos, sec_pos)

                # set two-swap mutation
                chrom_before_i = self.min_route_count + self.random_entity_count + self.entity_with_one_swap_mutation
                chrom_after_i = chrom_before_i + self.entity_with_two_swap_mutation

                for i in range(chrom_before_i, chrom_after_i):
                    # take minimal chromosome
                    self.drone_entity_list[i].chromosome = list(min_chromosome)

                    # swap two random gens
                    first_pos = random.randint(0, len(self.drone_entity_list[i].chromosome) - 1)
                    sec_pos = random.randint(0, len(self.drone_entity_list[i].chromosome) - 1)
                    self.drone_entity_list[i].swap_gens(first_pos, sec_pos)

                    # swap two random gens
                    first_pos = random.randint(0, len(self.drone_entity_list[i].chromosome) - 1)
                    sec_pos = random.randint(0, len(self.drone_entity_list[i].chromosome) - 1)
                    self.drone_entity_list[i].swap_gens(first_pos, sec_pos)

                for d in self.drone_entity_list:
                    d.set_route_length()
                    d.set_route_weight_and_penalty()

            # find minimal route
            min_ = self.drone_entity_list[0].length_route
            for d in self.drone_entity_list:
                if d.length_route <= min_:
                    min_chromosome = list(d.chromosome)
                    min_ = d.length_route

            self.draw_route(screen, min_chromosome, base)

            if last_min == min_:
                equal_counter += 1
            else:
                equal_counter = 0

            if equal_counter == 25:
                return {
                    "min": min_,
                    "route": transform_route(min_chromosome),
                    "generation": generation
                }

            print("gen = " + str(generation))
            print("minimal route length = " + str(min_))

            # reload
            self.set_drones_chromosome(base)

            # set minimal chromosome
            self.drone_entity_list[0].chromosome = list(min_chromosome)

    def draw_route(self, screen, route, base):
        colors = [
            (205, 92, 92),
            (255, 140, 0),
            (255, 160, 122),
            (0, 0, 128),
            (178, 34, 34),
            (255, 182, 193),
            (255, 20, 147),
            (255, 127, 80),
            (0, 255, 255),
            (221, 160, 221),
            (255, 0, 255),
            (75, 0, 130),
            (205, 92, 92),
            (255, 140, 0),
            (255, 160, 122),
            (0, 0, 128),
            (178, 34, 34),
            (255, 182, 193),
            (255, 20, 147),
            (255, 127, 80),
            (255, 215, 0),
            (221, 160, 221),
            (255, 0, 255),
            (75, 0, 130),
            (205, 92, 92),
            (255, 140, 0),
            (255, 160, 122),
            (0, 0, 128),
            (178, 34, 34),
            (255, 182, 193),
            (255, 20, 147),
            (255, 127, 80),
            (255, 215, 0),
            (221, 160, 221),
            (255, 0, 255),
            (75, 0, 130),
            (205, 92, 92),
            (255, 140, 0),
            (255, 160, 122),
            (0, 0, 128),
            (178, 34, 34),
            (255, 182, 193),
            (255, 20, 147),
            (255, 127, 80),
            (255, 215, 0),
            (221, 160, 221),
            (255, 0, 255),
            (75, 0, 130),
            (205, 92, 92),
            (255, 140, 0),
            (255, 160, 122),
            (0, 0, 128),
            (178, 34, 34),
            (255, 182, 193),
            (255, 20, 147),
            (255, 127, 80),
            (255, 215, 0),
            (221, 160, 221),
            (255, 0, 255),
            (75, 0, 130),
            (205, 92, 92),
            (255, 140, 0),
            (255, 160, 122),
            (0, 0, 128),
            (178, 34, 34),
            (255, 182, 193),
            (255, 20, 147),
            (255, 127, 80),
            (255, 215, 0),
            (221, 160, 221),
            (255, 0, 255),
            (75, 0, 130),
        ]
        color = 0
        # to first point
        pygame.draw.line(screen, colors[color],
                         (base.x_coordinate,
                          base.y_coordinate),
                         (route[0].x_coordinate,
                          route[0].y_coordinate),
                         2)
        # route
        for i in range(len(route) - 1):
            if route[i].x_coordinate == base.x_coordinate and route[i].y_coordinate == base.y_coordinate:
                color += 1
            pygame.draw.line(screen, colors[color],
                             (route[i].x_coordinate,
                              route[i].y_coordinate),
                             (route[i + 1].x_coordinate,
                              route[i + 1].y_coordinate),
                             2)

        # to end point
        pygame.draw.line(screen, colors[color],
                         (route[len(route) - 1].x_coordinate,
                          route[len(route) - 1].y_coordinate),
                         (base.x_coordinate,
                          base.y_coordinate),
                         2)

        pygame.display.flip()

def set_base():
    base_x_coordinate = 700
    base_y_coordinate = 400
    base_weight = 0
    base_color = (255, 0, 0)
    base_size = 10
    base_index = 0
    base = vertex.Vertex(base_x_coordinate, base_y_coordinate, base_weight, base_index)
    base.default_color = base_color
    base.default_size = base_size
    return base


def alg(population, vertexes, swap_count):
    # +++++++++++++++++++++++++++++++++++++++++++++++++
    evolution_alg = EvolutionAlgorithm(population, swap_count)
    # set vertexes list
    index = 1
    for vertex_info in vertexes:
        evolution_alg.set_vertexes(vertex_info[0], vertex_info[1], vertex_info[2], index)
        index += 1

    # set load capacity
    evolution_alg.set_load_capacity()

    # set minimal drone val
    evolution_alg.set_drone_min_num()

    # create base vertex
    base = set_base()

    evolution_alg.set_drones_chromosome(base)
    return evolution_alg.run(base)


def plot_length_population(vertexes):
    length_vert = []
    population_vert = []
    print("======================")
    print("Plot Length(Population)")
    for population in range(100, 5001, 100):
        sr = 0
        for i in range(0, 10):
            sr += alg(population, vertexes)
        sr /= 10
        length_vert.append(sr)
        population_vert.append(population)
        print("Complete with " + str(population) + ", Sr = " + str(sr))

    plt.plot(population_vert, length_vert)
    plt.xlabel('population')
    plt.ylabel('length')
    plt.show()


def plot_time_population(vertexes):
    # +++++++++++++++++++++++++++++++++++++++++++++++++

    time_vert = []
    population_vert = []
    print("======================")
    print("Plot Time(Population)")
    for population in range(100, 5001, 100):
        sr = 0
        for i in range(0, 10):
            start_time = time.time()
            alg(population, vertexes)
            sr += time.time() - start_time
        sr /= 10
        time_vert.append(sr)
        population_vert.append(population)
        print("Complete with " + str(population) + ", Sr = " + str(sr))

    plt.plot(population_vert, time_vert)
    plt.xlabel('population')
    plt.ylabel('time')
    plt.show()


def plot_brute_force_vs_mut_alg(verexes, population):
    print("==start==")
    vertex_num_list = []
    time_mut_list = []
    time_bf_list = []
    for i in range(1, 13):
        vertexes_send = []
        for j in range(0, i):
            vertexes_send.append(verexes[i])

        time_mut_alg = time.time()
        alg(population, vertexes_send)
        time_mut_res = time.time() - time_mut_alg

        time_bf_alg = time.time()

        route_list = []
        perm_iterator = itertools.permutations(list(vertexes_send))
        for j in perm_iterator:
            route_list.append(j)

        time_bf_res = time.time() - time_bf_alg

        print(time_bf_res)

        vertex_num_list.append(i)
        time_bf_list.append(time_bf_res)
        time_mut_list.append(time_mut_res)

        print("Complete with " + str(i + 1) + " points")

    print(time_bf_list)
    print(time_mut_list)

    plt.plot(vertex_num_list, time_bf_list, color='red', label='enume')
    plt.plot(vertex_num_list, time_mut_list, color='green', label='mutation')

    plt.xlabel('points')
    plt.ylabel('time')

    plt.legend()

    plt.show()


def set_optimal_population_set_between_random_and_swap(vertexes, population):
    attempt = 4
    start_count_with_swap = 0
    percent_list = []
    time_list = []

    for i in range(0, 400):
        start_count_with_swap += 5
        percent_swap = (start_count_with_swap / population) * 100
        sr = 0

        for j in range(0, attempt):
            start_time = time.time()
            alg(population, vertexes, start_count_with_swap)
            sr += time.time() - start_time

        sr /= attempt

        percent_list.append(percent_swap)
        time_list.append(sr)

        print("=> complete with " + str(percent_swap) + "-% swap mutation")

    plt.plot(percent_list, time_list)
    plt.xlabel('percent swap-mutation')
    plt.ylabel('time')
    plt.show()


def start(vertexes):
    optimal_value = 2000
    optimal_swap = 1200
    # set_optimal_population_set_between_random_and_swap(vertexes, optimal_value)
    return alg(optimal_value, vertexes, optimal_swap)
