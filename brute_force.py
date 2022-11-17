import itertools

import vertex


def print_vertexes(vertexes_to_print):
    for v in vertexes_to_print:
        print("====================")
        # print("x = " + str(v.x_coordinate))
        # print("y = " + str(v.y_coordinate))
        # print("weight = " + str(v.weight))
        print("index = " + str(v.index))


def set_base(start_route, additional_vertex_num):
    base_x_coordinate = 700
    base_y_coordinate = 400
    base_index = 0
    base_weight = 0
    base = vertex.Vertex(base_x_coordinate, base_y_coordinate, base_weight, base_index)

    for i in range(0, int(additional_vertex_num)):
        start_route.append(base)

    return list(start_route)


def take_vertex_by_index(start_route, index):
    for v in start_route:
        if v.index == index:
            return v


def calculate_length(start_route, route, base):
    # start route
    length = base.distance(take_vertex_by_index(start_route, route[0]))

    for i in range(0, len(route) - 1):
        length += take_vertex_by_index(start_route, route[i]).distance(take_vertex_by_index(start_route, route[i + 1]))

    length += take_vertex_by_index(start_route, route[len(route) - 1]).distance(base)

    return length


def calculate_penalty(start_route, route, base):
    weight = 0
    penalty = 0

    for v_index in route:
        if weight > 5:
            penalty += 10000

        weight += take_vertex_by_index(start_route, v_index).weight

        if take_vertex_by_index(start_route, v_index).x_coordinate == base.x_coordinate and take_vertex_by_index(
                start_route, v_index).y_coordinate == base.y_coordinate:
            weight = 0

    if weight > 5:
        penalty += 10000
    return penalty


def brute_force(start_route, base):
    index_vertex = []

    for v in start_route:
        index_vertex.append(v.index)

    route_list = []
    perm_iterator = itertools.permutations(list(index_vertex))
    for i in perm_iterator:
        route_list.append(i)

    length_list = []

    for route in route_list:
        length = calculate_length(start_route, route, base)
        length += calculate_penalty(start_route, route, base)
        length_list.append(length)

    min_ = 1000000
    for r_length in length_list:
        if r_length < min_:
            min_ = r_length
    print(min_)


def start(vertexes):
    start_route = []
    index = 0
    for v in vertexes:
        index += 1
        start_route.append(vertex.Vertex(v[0], v[1], v[2], index))

    weight_sum = 0
    for v in start_route:
        weight_sum += v.weight

    additional_vertex_num = len(vertexes)

    start_route = set_base(start_route, additional_vertex_num)

    base_x_coordinate = 700
    base_y_coordinate = 400
    base_index = 0
    base_weight = 0

    base = vertex.Vertex(base_x_coordinate, base_y_coordinate, base_weight, base_index)

    brute_force(start_route, base)
