import argparse
from copy import copy
from collections import namedtuple


Point = namedtuple("Point", "x y")
Portal = namedtuple("Portal", "name pos")
NAME_CHARS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
WALL_CHAR = '#'
PATH_CHAR = '.'
DIJKSTRA_INITIAL_DISTANCE = 99999


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    input_image = [[c for c in line[:-1]] for line in open(args.input_file) if len(line) > 1]
    shortest_distance, shortest_path = dijkstra(make_network(input_image, get_portals(input_image)), 'AA', 'ZZ')
    # There is also 1 step to move between portals
    print(f"Shortest path is {shortest_distance + len(shortest_path) - 2} steps")
    print(f"{' -> '.join(shortest_path)}")


def get_portals(image):
    def portal_at_point(x, y, x_step, y_step):
        if (image[y][x] in NAME_CHARS and image[y + y_step][x + x_step] in NAME_CHARS
                and image[y + 2 * y_step][x + 2 * x_step] == PATH_CHAR):
            name = image[y][x] + image[y + y_step][x + x_step]\
                if x_step > 0 or y_step > 0 else image[y + y_step][x + x_step] + image[y][x]
            return [Portal(name, Point(x + 2 * x_step, y + 2 * y_step))]
        else:
            return []
    portals = []
    for y in range(len(image)):
        for x in range(len(image[y])):
            if x < len(image[y]) - 2:
                portals += portal_at_point(x, y, 1, 0)
            if x >= 2:
                portals += portal_at_point(x, y, -1, 0)
            if y < len(image) - 2:
                portals += portal_at_point(x, y, 0, 1)
            if y >= 2:
                portals += portal_at_point(x, y, 0, -1)
    return portals


def make_network(maze_image, portals):
    points_to_portals = dict((p.pos, p) for p in portals)
    network = dict()
    for p in portals:
        if maze_image[p.pos.y][p.pos.x + 1] == PATH_CHAR:
            starting_point = Point(p.pos.x + 1, p.pos.y)
        elif maze_image[p.pos.y][p.pos.x - 1] == PATH_CHAR:
            starting_point = Point(p.pos.x - 1, p.pos.y)
        elif maze_image[p.pos.y + 1][p.pos.x] == PATH_CHAR:
            starting_point = Point(p.pos.x, p.pos.y + 1)
        elif maze_image[p.pos.y - 1][p.pos.x] == PATH_CHAR:
            starting_point = Point(p.pos.x, p.pos.y - 1)
        else:
            raise Exception("Can't find starting point!")
        portal_distances = get_portal_distances(
            get_portals_from_here(starting_point, maze_image, points_to_portals, {p.pos}, 1))
        if p.name in network:
            # Assume that you can't get to from one end of the portal to another just by walking
            network[p.name].update(portal_distances)
        else:
            network[p.name] = portal_distances
    return network


def get_portals_from_here(starting_point, maze_image, points_to_portals, already_traversed=None, num_prev_steps=0):
    if already_traversed is not None:
        ignored_points = copy(already_traversed)
    else:
        ignored_points = set()
    target_point = starting_point
    step_count = num_prev_steps
    while True:
        if target_point in points_to_portals:
            return [(points_to_portals[target_point], step_count)]
        possible_next_steps = (Point(target_point.x + 1, target_point.y), Point(target_point.x - 1, target_point.y),
                               Point(target_point.x, target_point.y + 1), Point(target_point.x, target_point.y - 1))
        valid_next_steps = [p for p in possible_next_steps if maze_image[p.y][p.x] == PATH_CHAR and p not in ignored_points]
        ignored_points.add(target_point)
        if len(valid_next_steps) == 0:
            return []
        elif len(valid_next_steps) > 1:
            portals_from_here = []
            for p in valid_next_steps:
                portals_from_here.extend(get_portals_from_here(p, maze_image, points_to_portals,
                                                               ignored_points, step_count + 1))
            return portals_from_here
        target_point = valid_next_steps[0]
        step_count += 1


def get_portal_distances(portal_distances_list):
    portal_distances = {}
    for portal, distance in portal_distances_list:
        if portal.name not in portal_distances or portal_distances[portal.name] > distance:
            portal_distances[portal.name] = distance
    return portal_distances


def dijkstra(graph, start_node, end_node):
    unvisited = set(graph.keys())
    shortest_distances = dict((name, 0 if name == start_node else DIJKSTRA_INITIAL_DISTANCE) for name in graph.keys())
    shortest_distance_neighbour = dict((name, None) for name in graph)
    current_node = None
    while len(unvisited) > 0:
        current_node = sorted(unvisited, key=lambda name: shortest_distances[name])[0]
        for neighbour in graph[current_node].keys():
            if neighbour in unvisited:
                if shortest_distances[neighbour] > shortest_distances[current_node] + graph[current_node][neighbour]:
                    shortest_distances[neighbour] = shortest_distances[current_node] + graph[current_node][neighbour]
                    shortest_distance_neighbour[neighbour] = current_node
        unvisited.remove(current_node)
    shortest_path_backtrack = [end_node]
    backtrack_node = end_node
    while backtrack_node != start_node:
        shortest_path_backtrack.append(shortest_distance_neighbour[backtrack_node])
        backtrack_node = shortest_distance_neighbour[backtrack_node]
    return shortest_distances[end_node], [x for x in reversed(shortest_path_backtrack)]


if __name__ == "__main__":
    main()
